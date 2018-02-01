import createReducer, {RESET_STORE} from '../createReducer'
import qs from 'query-string'
import {getToken} from './user'

// ------------------------------------
// Constants
// ------------------------------------
export const GET_DIAGNOSIS_DATA_REQUEST = 'Diagnosis.GET_DIAGNOSIS_DATA_REQUEST'
export const GET_DIAGNOSIS_DATA_SUCCESS = 'Diagnosis.GET_DIAGNOSIS_DATA_SUCCESS'
export const GET_DIAGNOSIS_DATA_FAILURE = 'Diagnosis.GET_DIAGNOSIS_DATA_FAILURE'

export const CLEAR = 'Diagnosis.CLEAR'

// ------------------------------------
// Actions
// ------------------------------------
export const getDiagnosisData = (values) => (dispatch, getState, {fetch, history}) => {
  dispatch({type: GET_DIAGNOSIS_DATA_REQUEST})
  const {token} = dispatch(getToken())
  return fetch(`/diagnosis/reports/?${qs.stringify(values)}`, {
    method: 'GET',
    token,
    success: (data) => {
      dispatch({type: GET_DIAGNOSIS_DATA_SUCCESS, data})
      history.push('/diagnosis')
    },
    failure: (err) => dispatch({type: GET_DIAGNOSIS_DATA_FAILURE})
  })
}

export const clear = () => ({type: CLEAR})

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
  loading: false,
  data: {},
}

export default createReducer(initialState, {
  [GET_DIAGNOSIS_DATA_REQUEST]: (state, action) => ({
    loading: true,
  }),
  [GET_DIAGNOSIS_DATA_SUCCESS]: (state, {data}) => ({
    loading: false,
    data,
  }),
  [GET_DIAGNOSIS_DATA_FAILURE]: (state, action) => ({
    loading: false,
  }),
  [CLEAR]: (state, action) => RESET_STORE,
})
