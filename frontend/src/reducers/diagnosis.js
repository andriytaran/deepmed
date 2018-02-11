import createReducer, {RESET_STORE} from '../createReducer'
import {getToken} from './user'
import {WS_CONNECT, WS_OPEN, WS_SEND} from '../store/socketMiddleware'

// ------------------------------------
// Constants
// ------------------------------------
export const GET_DIAGNOSIS_REQUEST = 'Diagnosis.GET_DIAGNOSIS_REQUEST'
export const GET_DIAGNOSIS_SUCCESS = 'Diagnosis.GET_DIAGNOSIS_SUCCESS'
export const GET_DIAGNOSIS_FAILURE = 'Diagnosis.GET_DIAGNOSIS_FAILURE'

export const GET_SIMILAR_DIAGNOSES_REQUEST = 'Diagnosis.GET_SIMILAR_DIAGNOSES_REQUEST'
export const GET_SIMILAR_DIAGNOSES_SUCCESS = 'Diagnosis.GET_SIMILAR_DIAGNOSES_SUCCESS'
export const GET_SIMILAR_DIAGNOSES_FAILURE = 'Diagnosis.GET_SIMILAR_DIAGNOSES_FAILURE'

export const GET_INDIVIDUAL_STATISTICS_REQUEST = 'Diagnosis.GET_INDIVIDUAL_STATISTICS_REQUEST'
export const GET_INDIVIDUAL_STATISTICS_SUCCESS = 'Diagnosis.GET_INDIVIDUAL_STATISTICS_SUCCESS'
export const GET_INDIVIDUAL_STATISTICS_FAILURE = 'Diagnosis.GET_INDIVIDUAL_STATISTICS_FAILURE'

export const CLEAR = 'Diagnosis.CLEAR'

const DIAGNOSIS = '/diagnosis/'
const SIMILAR_DIAGNOSES = '/similar-diagnoses/'
const INDIVIDUAL_STATISTICS = '/individual-statistics/'

// ------------------------------------
// Actions
// ------------------------------------
export const wsConnect = () => (dispatch, getState) => {
  const {wsConnected} = getState().diagnosis
  if (process.env.BROWSER && !wsConnected) {
    const {token} = dispatch(getToken())
    dispatch({
      type: WS_CONNECT,
      path: DIAGNOSIS,
      query: {token},
      success: (data) => dispatch({type: GET_DIAGNOSIS_SUCCESS, data}),
      failure: () => dispatch({type: GET_DIAGNOSIS_FAILURE}),
    })
    dispatch({
      type: WS_CONNECT,
      path: SIMILAR_DIAGNOSES,
      query: {token},
      success: (data) => dispatch({type: GET_SIMILAR_DIAGNOSES_SUCCESS, data}),
      failure: () => dispatch({type: GET_SIMILAR_DIAGNOSES_FAILURE}),
    })
    dispatch({
      type: WS_CONNECT,
      path: INDIVIDUAL_STATISTICS,
      query: {token},
      success: (data) => dispatch({type: GET_INDIVIDUAL_STATISTICS_SUCCESS, data}),
      failure: () => dispatch({type: GET_INDIVIDUAL_STATISTICS_FAILURE}),
    })
  }
}

export const getData = (values) => (dispatch, getState, {history}) => {
  if (process.env.BROWSER) {
    dispatch(getDiagnosis(values))
    dispatch(getSimilarDiagnoses(values))
    dispatch(getIndividualStatistics(values))
    history.push('/diagnosis')
  }
}

export const getDiagnosis = (values) => (dispatch, getState) => {
  const {token} = dispatch(getToken())
  dispatch({type: GET_DIAGNOSIS_REQUEST, diagnosisForm: values})
  dispatch({type: WS_SEND, path: DIAGNOSIS, query: {token}, message: values})
}

export const getSimilarDiagnoses = (values) => (dispatch, getState) => {
  const {token} = dispatch(getToken())
  dispatch({type: GET_SIMILAR_DIAGNOSES_REQUEST})
  dispatch({type: WS_SEND, path: INDIVIDUAL_STATISTICS, query: {token}, message: values})
}

export const getIndividualStatistics = (values) => (dispatch, getState) => {
  const {token} = dispatch(getToken())
  dispatch({type: GET_INDIVIDUAL_STATISTICS_REQUEST})
  dispatch({type: WS_SEND, path: SIMILAR_DIAGNOSES, query: {token}, message: values})
}

export const clear = () => ({type: CLEAR})

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
  loading: false,
  diagnosisForm: {},
  diagnosis: {},
  similarDiagnoses: {},
  individualStatistics: {},
  wsConnected: false,
}

export default createReducer(initialState, {
  [GET_DIAGNOSIS_REQUEST]: (state, {diagnosisForm}) => ({
    loading: true,
    diagnosisForm,
    diagnosis: {},
  }),
  [WS_OPEN]: (state, action) => ({
    wsConnected: true,
  }),
  [GET_DIAGNOSIS_SUCCESS]: (state, {data}) => ({
    loading: false,
    diagnosis: {
      ...state.diagnosis,
      ...data,
    },
  }),
  [GET_DIAGNOSIS_FAILURE]: (state, action) => ({
    loading: false,
  }),
  [GET_SIMILAR_DIAGNOSES_REQUEST]: (state, action) => ({
    similarDiagnoses: {},
  }),
  [GET_SIMILAR_DIAGNOSES_SUCCESS]: (state, {data}) => ({
    similarDiagnoses: {
      ...state.similarDiagnoses,
      ...data,
    },
  }),
  [GET_INDIVIDUAL_STATISTICS_REQUEST]: (state, action) => ({
    individualStatistics: {},
  }),
  [GET_INDIVIDUAL_STATISTICS_SUCCESS]: (state, {data}) => ({
    individualStatistics: {
      ...state.individualStatistics,
      ...data,
    },
  }),
  [CLEAR]: (state, action) => RESET_STORE,
})
