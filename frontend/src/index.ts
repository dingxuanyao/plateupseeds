import { S3Client, ListObjectsCommand } from "@aws-sdk/client-s3";
// import 'dotenv/config';
const REGION = "us-east-1";
const s3Configuration = {
  credentials: {
    accessKeyId:  process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  },
  region: REGION,
};
const s3 = new S3Client(s3Configuration);

function getHtml(template) {
  return template.join("\n");
}

function stripFileExtension(filename) {
  if (filename.endsWith(".png") || filename.endsWith(".jpg")) {
    return filename.substring(0, filename.length - 4);
  }
  return filename;
}

function getSeedName(s3_path) {
  let tmp = s3_path.split("/");
  let filename = tmp[tmp.length - 1];
  return stripFileExtension(filename);
}
// Make the getHTML function available to the browser
window.getHTML = getHtml;

// List the photo albums that exist in the bucket
var s3BucketName = "album-test-939326176859"; //BUCKET_NAME

function cardHtml(photoUrl, photoKey, index) {
  var href = "https://plateupseeds.com/";
  var seedname = getSeedName(photoKey);
  var photoUrlOriginal = href + encodeURIComponent("seeds_sorted/high_quality/" + seedname + ".jpg");

  // creates a placeholder location so that the image doesn't jump around when it loads
  // div creates a 5:4 space for the image
  // image rests on top and left
  // alternatives welcome
  var html = `
<div class="col-lg-2 col-sm-4 p-0" >
  <div class="card text-white bg-dark text-center border-secondary m-1 btn" data-bs-toggle="modal" data-bs-target="#exampleModal" data-bs-photourl="${photoUrlOriginal}">
    <div class="card-body">
    <div style="width:100%;height:0; padding-top:80%;position:relative;">
    <img src="${photoUrl}" class="card-img-top" alt="Responsive image" loading="lazy" style="position:absolute; top:0; left:0; width:100%;"/>
    </div>
      <div class="card-text">${getSeedName(photoKey)}</div>
    </div>
  </div>
</div>
`;
  return html;
}

const renderSeeds = async (img_type) => {
  try {
    const seedPrefix = "seeds_sorted/" + img_type + "/";
    var href = "https://plateupseeds.com/";
    var previewHtmlTemplate = [];
    var htmlTemplate = [];
    const data = await s3.send(
      new ListObjectsCommand({
        Bucket: s3BucketName,
        Prefix: seedPrefix,
      })
    ).then((data) => {
      data.Contents.map(function (photo, index) {
        var photoKey = photo.Key;
        var photoUrl = href + encodeURIComponent(photoKey);
        var html = cardHtml(photoUrl, photoKey, index);
        if (index < 6) {
          previewHtmlTemplate.push(html);
        } else {
          htmlTemplate.push(html);
        }
      });
      const previewElement = "seed-" + img_type + "-preview";
      document.getElementById(previewElement).innerHTML = getHtml(previewHtmlTemplate);
      const element = "seed-" + img_type;
      document.getElementById(element).innerHTML = getHtml(htmlTemplate);
    });
  } catch (err) {
    console.log("Error", err);
  }
};

window.renderSeeds = renderSeeds;
export {
  renderSeeds,
};
