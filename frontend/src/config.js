/* eslint-disable max-len */

if (process.env.BROWSER) {
  throw new Error('Do not import `config.js` from inside the client-side code.')
}

module.exports = {
  // Node.js app
  port: process.env.PORT || 3000,

  // API Gateway
  api: {
    url: process.env.API_URL || 'http://api-portal.deepmed.com/api',
    ws: process.env.WS_URL || 'ws://api-portal.deepmed.com/ws/api',
    // oauth keys
    clientId: process.env.CLIENT_ID || '',
    clientSecret: process.env.CLIENT_SECRET || '',
  },

  appUrl: process.env.APP_URL || 'http://localhost:3000',
  googleClientId: process.env.GOOGLE_CLIENT_ID || '',

  // Web analytics
  analytics: {
    // https://analytics.google.com/
    googleTrackingId: process.env.GOOGLE_TRACKING_ID || 'UA-114674796-1', // UA-XXXXX-X
  },
}
