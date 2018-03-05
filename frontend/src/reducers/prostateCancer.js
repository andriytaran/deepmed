import createReducer, {RESET_STORE} from '../createReducer'
import {getToken} from './user'
import {WS_CONNECT, WS_OPEN, WS_SEND} from '../store/socketMiddleware'
import qs from 'query-string'

// ------------------------------------
// Constants
// ------------------------------------
export const CLEAR = 'Diagnosis.CLEAR'


// ------------------------------------
// Actions
// ------------------------------------


export const clear = () => ({type: CLEAR})

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
  loading: false,
  diagnosisForm: {},
}

export default createReducer(initialState, {
  [CLEAR]: (state, action) => RESET_STORE,
})
