import {
    FETCH_REPORT_DATA_REQUEST,
    FETCH_REPORT_DATA_SUCCESS,
    FETCH_REPORT_DATA_FAILURE
} from '../constants';

const initialState = {
    data: null,
    isFetching: false
};

export default function reportReducer(state = initialState, action) {
    switch (action.type) {
        case FETCH_REPORT_DATA_SUCCESS:
            return Object.assign({}, state, {
                data: action.payload.data,
                isFetching: false
            });

        case FETCH_REPORT_DATA_FAILURE:
            return Object.assign({}, state, {
                isFetching: false
            });

        case FETCH_REPORT_DATA_REQUEST:
            return Object.assign({}, state, {
                isFetching: true
            });
        default:
            return state;
    }
}
