import createReducer, {RESET_STORE} from '../createReducer'
import {setCookie} from 'redux-cookie'
import {getUser} from './user'
import {WEEK} from '../constants'

// ------------------------------------
// Constants
// ------------------------------------
export const LOGIN_REQUEST = 'Login.LOGIN_REQUEST'
export const LOGIN_SUCCESS = 'Login.LOGIN_SUCCESS'
export const LOGIN_FAILURE = 'Login.LOGIN_FAILURE'

export const ACTIVATE_REQUEST = 'Login.ACTIVATE_REQUEST'
export const ACTIVATE_SUCCESS = 'Login.ACTIVATE_SUCCESS'
export const ACTIVATE_FAILURE = 'Login.ACTIVATE_FAILURE'

export const CLEAR = 'Login.CLEAR'

// ------------------------------------
// Actions
// ------------------------------------
export const login = (values, redirectUrl) => (dispatch, getState, {fetch}) => {
  dispatch({type: LOGIN_REQUEST})
  const {clientId, clientSecret} = getState().global
  return fetch(`/auth/token/`, {
    method: 'POST',
    formData: true,
    body: {
      username: values.email,
      password: values.password,
      grant_type: 'password',
      client_id: clientId,
      client_secret: clientSecret,
    },
    success: (res) => dispatch(loginSuccess(res, redirectUrl)),
    failure: (err) => dispatch({type: LOGIN_FAILURE, error: 'Something went wrong. Please try again.'})
  })
}

export const loginSuccess = (auth, redirectUrl = '/') => (dispatch, getState, {history}) => {
  dispatch({type: LOGIN_SUCCESS})
  dispatch(setCookie('token', auth.access_token, {expires: auth.expires_in}))
  dispatch(setCookie('refresh_token', auth.refresh_token, {expires: WEEK}))
  dispatch(setCookie('prev_token', auth.access_token, {expires: WEEK}))
  dispatch(getUser())
  history.push(redirectUrl)
}

export const activate = (key) => (dispatch, getState, {fetch, history}) => {
  dispatch({type: ACTIVATE_REQUEST})
  return fetch(`/user/activate/`, {
    method: 'PUT',
    body: {
      key,
    },
    success: (res) => {
      dispatch({type: ACTIVATE_SUCCESS, success: 'success'})
      // to prevent redirecting on server
      if (process.env.BROWSER) {
        // TODO use route
        history.replace('/login')
      }
    },
    failure: (err) => {
      dispatch({type: ACTIVATE_FAILURE, error: 'error'})
      // to prevent redirecting on server
      if (process.env.BROWSER) {
        history.replace('/login')
      }
    },
  })
}

export const clear = () => ({type: CLEAR})

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
  loading: false,
  error: null,
  success: null,
}

export default createReducer(initialState, {
  [LOGIN_REQUEST]: (state, action) => ({
    loading: true,
    success: null,
    error: null,
  }),
  [LOGIN_SUCCESS]: (state, action) => ({
    loading: false,
    error: null,
  }),
  [LOGIN_FAILURE]: (state, {error}) => ({
    loading: false,
    error,
  }),
  [ACTIVATE_REQUEST]: (state, action) => ({
    success: null,
    error: null,
  }),
  [ACTIVATE_SUCCESS]: (state, {success}) => ({
    success,
    error: null,
  }),
  [ACTIVATE_FAILURE]: (state, {error}) => ({
    success: null,
    error,
  }),
  [CLEAR]: (state, action) => RESET_STORE,
})
