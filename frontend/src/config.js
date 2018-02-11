/* eslint-disable max-len */

if (process.env.BROWSER) {
  throw new Error('Do not import `config.js` from inside the client-side code.')
}

module.exports = {
  // Node.js app
  port: process.env.PORT || 3000,

  // API Gateway
  api: {
    url: process.env.API_URL || 'http://52.14.12.34:8000/api',
    ws: process.env.WS_URL || 'ws://52.14.12.34:8000/ws/api',
    // oauth keys
    clientId: process.env.CLIENT_ID || '4XnsRtTGMUp1TO3WCniWsl5THzLNmjcfqU5Keh5C',
    clientSecret: process.env.CLIENT_SECRET || 'ugpViM0R277iKi70ZMB9PI126gFygDkHau7Ztf11L9yuQ9c8uWIzXExhoMetgJpV1YAS9szAsjs6KmCM4IIl8Y5zFhmUDBfj07o7nUCQp2MmM66GBvn3lvSCY3z2WfPn',
  },

  appUrl: process.env.APP_URL || 'http://localhost:3000',

  // Web analytics
  analytics: {
    // https://analytics.google.com/
    googleTrackingId: process.env.GOOGLE_TRACKING_ID, // UA-XXXXX-X
  },
}
