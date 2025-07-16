// Native Android accessibility service stub
const AccessibilityService = {
  start(): Promise<string> {
    return Promise.resolve('Accessibility service started');
  },
  stop(): Promise<string> {
    return Promise.resolve('Accessibility service stopped');
  },
};

export default AccessibilityService;