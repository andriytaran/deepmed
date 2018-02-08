import createReducer, {RESET_STORE} from '../createReducer'
import qs from 'query-string'
import {getToken} from './user'

// ------------------------------------
// Constants
// ------------------------------------
export const GET_DIAGNOSIS_DATA_REQUEST = 'Diagnosis.GET_DIAGNOSIS_DATA_REQUEST'
export const GET_DIAGNOSIS_DATA_SUCCESS = 'Diagnosis.GET_DIAGNOSIS_DATA_SUCCESS'
export const GET_DIAGNOSIS_DATA_FAILURE = 'Diagnosis.GET_DIAGNOSIS_DATA_FAILURE'

export const GET_CHART_DATA_REQUEST = 'Diagnosis.GET_CHART_DATA_REQUEST'
export const GET_CHART_DATA_SUCCESS = 'Diagnosis.GET_CHART_DATA_SUCCESS'
export const GET_CHART_DATA_FAILURE = 'Diagnosis.GET_CHART_DATA_FAILURE'

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
      dispatch({type: GET_DIAGNOSIS_DATA_SUCCESS, data, diagnosisForm: values})
      history.push('/diagnosis')
      dispatch(getChartData(values))
    },
    failure: (err) => dispatch({type: GET_DIAGNOSIS_DATA_FAILURE})
  })
}

export const getChartData = (values) => (dispatch, getState, {fetch, history}) => {
  dispatch({type: GET_CHART_DATA_REQUEST})
  const {token} = dispatch(getToken())
  return fetch(`/diagnosis/chart/?${qs.stringify(values)}`, {
    method: 'GET',
    token,
    success: (chartData) => dispatch({type: GET_CHART_DATA_SUCCESS, chartData}),
    failure: (err) => dispatch({type: GET_CHART_DATA_FAILURE})
  })
}

export const clear = () => ({type: CLEAR})

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
  loading: false,
  diagnosisForm: {},
  data: {},
  chartData: {},
}

export default createReducer(initialState, {
  [GET_DIAGNOSIS_DATA_REQUEST]: (state, action) => ({
    loading: true,
  }),
  [GET_DIAGNOSIS_DATA_SUCCESS]: (state, {data, diagnosisForm}) => ({
    loading: false,
    data,
    diagnosisForm,
  }),
  [GET_DIAGNOSIS_DATA_FAILURE]: (state, action) => ({
    loading: false,
  }),
  [GET_CHART_DATA_SUCCESS]: (state, {chartData}) => ({
    chartData,
  }),
  [CLEAR]: (state, action) => RESET_STORE,
})
