import createReducer, {RESET_STORE} from '../createReducer'
import {getCookie, removeCookie} from 'redux-cookie'
import {loginSuccess} from './login'

// ------------------------------------
// Constants
// ------------------------------------
export const LOGOUT_REQUEST = 'User.LOGOUT_REQUEST'
export const LOGOUT_SUCCESS = 'User.LOGOUT_SUCCESS'
export const LOGOUT_FAILURE = 'User.LOGOUT_FAILURE'

export const GET_USER_REQUEST = 'User.GET_USER_REQUEST'
export const GET_USER_SUCCESS = 'User.GET_USER_SUCCESS'
export const GET_USER_FAILURE = 'User.GET_USER_FAILURE'

export const REFRESH_TOKEN_REQUEST = 'User.REFRESH_TOKEN_REQUEST'
export const REFRESH_TOKEN_SUCCESS = 'User.REFRESH_TOKEN_SUCCESS'
export const REFRESH_TOKEN_FAILURE = 'User.REFRESH_TOKEN_FAILURE'

// ------------------------------------
// Actions
// ------------------------------------
export const expireToken = () => (dispatch, getState) => {
  dispatch(removeCookie('token', {path: ''}))
  dispatch(removeCookie('refresh_token', {path: ''}))
  dispatch(removeCookie('prev_token', {path: ''}))
}

export const logoutSuccess = () => (dispatch) => {
  dispatch(expireToken())
  dispatch({type: LOGOUT_SUCCESS})
}

export const refreshToken = (token, refresh_token) => (dispatch, getState, {fetch, history}) => {
  const {refreshingToken} = getState().user
  if (refreshingToken) {
    return
  }
  dispatch({type: REFRESH_TOKEN_REQUEST})
  const {clientId, clientSecret, currentPathname} = getState().global
  return fetch(`/auth/token/`, {
    method: 'POST',
    contentType: 'application/x-www-form-urlencoded',
    body: {
      client_id: clientId,
      client_secret: clientSecret,
      grant_type: 'refresh_token',
      refresh_token,
    },
    success: (res) => {
      dispatch(loginSuccess(res, true, currentPathname))
      dispatch({type: REFRESH_TOKEN_SUCCESS})
    },
    failure: (err) => {
      dispatch(logoutSuccess())
      dispatch({type: REFRESH_TOKEN_FAILURE})
      if (process.env.BROWSER) {
        // refresh page to resend requests
        history.replace(currentPathname)
      }
    }
  })
}

export const getToken = () => (dispatch, getState, {history}) => {
  const {currentPathname} = getState().global
  const {loggedIn} = getState().user
  const token = dispatch(getCookie('token'))
  const refresh_token = dispatch(getCookie('refresh_token'))
  const prevToken = dispatch(getCookie('prev_token'))
  if (!token) {
    if (prevToken && refresh_token) {
      dispatch(refreshToken(prevToken, refresh_token))
    } else if (loggedIn) {
      dispatch(logoutSuccess())
      if (process.env.BROWSER) {
        // refresh page to resend requests
        history.replace(currentPathname)
      }
    }
    return {}
  }
  return {token, refresh_token}
}

export const logout = (redirectUrl) => (dispatch, getState, {fetch}) => {
  const {clientId, clientSecret} = getState().global
  const {token} = dispatch(getToken())
  dispatch({type: LOGOUT_REQUEST})
  return fetch(`/auth/revoke-token/`, {
    method: 'POST',
    contentType: 'application/x-www-form-urlencoded',
    token,
    body: {
      client_id: clientId,
      client_secret: clientSecret,
      token,
    },
    success: (res) => dispatch(logoutSuccess(res)),
    failure: (err) => dispatch({type: LOGOUT_FAILURE, err})
  })
}

export const getUser = () => (dispatch, getState, {fetch}) => {
  const {token} = dispatch(getToken())
  const {user} = getState().user
  if (!user && token) {
    dispatch({type: GET_USER_REQUEST})
    return fetch(`/accounts/user/me/`, {
      method: 'GET',
      token,
      success: (res) => dispatch({type: GET_USER_SUCCESS, user: res}),
      failure: (err) => dispatch({type: GET_USER_FAILURE, error: err})
    })
  } else {
    return user
  }
}

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
  loading: false,
  loggedIn: false,
  error: null,
  user: null,
  refreshingToken: false,
}

export default createReducer(initialState, {
  [LOGOUT_SUCCESS]: (state, action) => RESET_STORE,
  [LOGOUT_FAILURE]: (state, {error}) => ({
    error,
  }),
  [GET_USER_SUCCESS]: (state, {user}) => ({
    user,
    loggedIn: true,
  }),
  [REFRESH_TOKEN_REQUEST]: (state, action) => ({
    refreshingToken: true,
  }),
  [REFRESH_TOKEN_SUCCESS]: (state, action) => ({
    refreshingToken: false,
  }),
  [REFRESH_TOKEN_FAILURE]: (state, action) => ({
    refreshingToken: false,
  }),
})
