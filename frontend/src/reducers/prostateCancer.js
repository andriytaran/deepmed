import createReducer, {RESET_STORE} from '../createReducer'
import {getToken} from './user'
import {WS_CONNECT, WS_OPEN, WS_SEND} from '../store/socketMiddleware'
import {CLEAR} from './breastCancer';
import qs from 'query-string'

// ------------------------------------
// Constants
// ------------------------------------
export const GET_PROSTATE_INDIVIDUAL_STATISTICS_REQUEST = 'Diagnosis.Prostate.GET_INDIVIDUAL_STATISTICS_REQUEST';
export const GET_PROSTATE_INDIVIDUAL_STATISTICS_SUCCESS = 'Diagnosis.Prostate.GET_INDIVIDUAL_STATISTICS_SUCCESS';
export const GET_PROSTATE_INDIVIDUAL_STATISTICS_FAILURE = 'Diagnosis.Prostate.GET_INDIVIDUAL_STATISTICS_FAILURE';

export const PROSTATE_INDIVIDUAL_STATISTICS = '/pc-module/individual-statistics/';

// ------------------------------------
// Actions
// ------------------------------------

export const getData = (values) => (dispatch, getState, {history}) => {
  if (process.env.BROWSER) {
    dispatch(getIndividualStatistics(values));
    // TODO use route name instead
    history.push('/prostate-cancer/individual-statistics')
  }
};

const getIndividualStatistics = (values) => (dispatch, getState) => {
  const {token} = dispatch(getToken());
  dispatch({type: GET_PROSTATE_INDIVIDUAL_STATISTICS_REQUEST});
  dispatch({type: WS_SEND, path: PROSTATE_INDIVIDUAL_STATISTICS, query: {token}, message: values})
};



// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
  loading: false,
  diagnosisForm: {},
  individualStatistics: {},
  wsConnected: false,
};

export default createReducer(initialState, {
  [CLEAR]: (state, action) => RESET_STORE,
  [WS_OPEN]: (state, action) => ({
    wsConnected: true,
  }),
  [GET_PROSTATE_INDIVIDUAL_STATISTICS_REQUEST]: (state, action) => ({
    individualStatistics: {},
  }),
  [GET_PROSTATE_INDIVIDUAL_STATISTICS_SUCCESS]: (state, {data}) => ({
    individualStatistics: {
      ...state.individualStatistics,
      ...data,
    },
  }),
})
