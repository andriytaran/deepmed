import fetch from 'isomorphic-fetch';
import { push } from 'react-router-redux';

import { SERVER_URL } from '../utils/config';
import { checkHttpStatus, parseJSON } from '../utils';
import { SUBMIT_DIAGNOSIS_DATA_REQUEST, SUBMIT_DIAGNOSIS_DATA_SUCCESS, SUBMIT_DIAGNOSIS_DATA_FAILURE } from '../constants';
import { authLoginUserFailure } from './auth';


export function submitDiagnosisDataSuccess(data) {
    return {
        type: SUBMIT_DIAGNOSIS_DATA_SUCCESS,
        payload: {
            data
        }
    };
}

export function submitDiagnosisDataRequest() {
    return {
        type: SUBMIT_DIAGNOSIS_DATA_REQUEST
    };
}

export function submitDiagnosisDataFailure() {
    return {
        type: SUBMIT_DIAGNOSIS_DATA_FAILURE
    };
}

export function submitDiagnosisData(token, values) {
    return (dispatch, state) => {
        dispatch(submitDiagnosisDataRequest());
        return fetch(`${SERVER_URL}/api/v1/getdata/`, {
            credentials: 'include',
            headers: {
                Accept: 'application/json',
                Authorization: `Token ${token}`
            }
        })
            .then(checkHttpStatus)
            .then(parseJSON)
            .then((response) => {
                dispatch(submitDiagnosisDataSuccess(response.data));
                dispatch(push('/diagnosis'));
            })
            .catch((error) => {
                dispatch(submitDiagnosisDataFailure(error.response));
                if (error && typeof error.response !== 'undefined' && error.response.status === 401) {
                    // Invalid authentication credentials
                    return error.response.json().then((data) => {
                        dispatch(authLoginUserFailure(401, data.non_field_errors[0]));
                        dispatch(push('/login'));
                    });
                } else if (error && typeof error.response !== 'undefined' && error.response.status >= 500) {
                    // Server side error
                    dispatch(authLoginUserFailure(500, 'A server error occurred while sending your data!'));
                } else {
                    // Most likely connection issues
                    dispatch(authLoginUserFailure('Connection Error', 'An error occurred while sending your data!'));
                }

                dispatch(push('/login'));
                return Promise.resolve();
            });
    };
}
