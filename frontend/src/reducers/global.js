import createReducer from '../createReducer'

// ------------------------------------
// Constants
// ------------------------------------
// TODO
const MODULES = ['bc']

export const SET_CURRENT_PATHNAME = 'Global.SET_CURRENT_PATHNAME'
export const SET_CURRENT_ROUTE_NAME = 'Global.SET_CURRENT_ROUTE_NAME'
export const SET_QUERY = 'Global.SET_QUERY'

export const SET_CONFIG_VARS = 'Global.SET_CONFIG_VARS'

export const TOGGLE_SIDEBAR_OPENED = 'Global.TOGGLE_SIDEBAR_OPENED'

// ------------------------------------
// Actions
// ------------------------------------
export const setConfigVars = ({clientId, clientSecret, googleTrackingId, googleClientId, apiUrl, appUrl, apiBaseUrl, wsUrl}) => ({
  type: SET_CONFIG_VARS,
  clientId,
  clientSecret,
  googleTrackingId,
  googleClientId,
  apiUrl,
  appUrl,
  apiBaseUrl,
  wsUrl,
})

export const setCurrentPathname = (currentPathname) => ({type: SET_CURRENT_PATHNAME, currentPathname})

export const setQuery = (query) => ({type: SET_QUERY, query})

export const setCurrentRouteName = (currentRouteName) => {
  // TODO
  const routeNamePrefix = currentRouteName.split('-')[0]
  const isModule = MODULES.includes(routeNamePrefix)
  return ({type: SET_CURRENT_ROUTE_NAME, currentRouteName, currentModule: isModule ? routeNamePrefix : null})
}

export const toggleSidebarOpened = () => ({type: TOGGLE_SIDEBAR_OPENED})

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
  currentPathname: null,
  currentRouteName: null,
  clientId: null,
  clientSecret: null,
  apiUrl: null,
  appUrl: null,
  apiBaseUrl: null,
  wsUrl: null,
  googleClientId: null,
  query: {},
  sidebarOpened: false,
  currentModule: null,
}

export default createReducer(initialState, {
  [SET_CURRENT_PATHNAME]: (state, {currentPathname}) => ({
    currentPathname,
  }),
  [SET_CURRENT_ROUTE_NAME]: (state, {currentRouteName, currentModule}) => ({
    currentRouteName,
    currentModule,
  }),
  [SET_QUERY]: (state, {query}) => ({
    query,
  }),
  [TOGGLE_SIDEBAR_OPENED]: (state, action) => ({
    sidebarOpened: !state.sidebarOpened,
  }),
  [SET_CONFIG_VARS]: (state, {clientId, clientSecret, googleTrackingId, googleClientId, apiUrl, appUrl, apiBaseUrl, wsUrl}) => ({
    clientId,
    clientSecret,
    googleTrackingId,
    googleClientId,
    apiUrl,
    appUrl,
    apiBaseUrl,
    wsUrl,
  }),
})
