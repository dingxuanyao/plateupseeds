export { };

declare global {
  interface Window {
    getHTML: any;
    renderSeeds: any;
  }
  interface ProcessEnv {
    AWS_ACCESS_KEY_ID: string;
    AWS_SECRET_ACCESS_KEY: string;
    NODE_ENV: 'development' | 'production';
  }
}
