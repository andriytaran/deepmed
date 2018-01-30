import {
    SUBMIT_DIAGNOSIS_DATA_REQUEST,
    SUBMIT_DIAGNOSIS_DATA_SUCCESS,
    SUBMIT_DIAGNOSIS_DATA_FAILURE
} from '../constants';

const initialState = {
    data: null,
    isFetching: false
};

export default function dataReducer(state = initialState, action) {
    switch (action.type) {
        case SUBMIT_DIAGNOSIS_DATA_SUCCESS:
            return Object.assign({}, state, {
                data: action.payload.data,
                isFetching: false
            });

        case SUBMIT_DIAGNOSIS_DATA_FAILURE:
            return Object.assign({}, state, {
                isFetching: false
            });

        case SUBMIT_DIAGNOSIS_DATA_REQUEST:
            return Object.assign({}, state, {
                isFetching: true
            });
        default:
            return state;
    }
}
