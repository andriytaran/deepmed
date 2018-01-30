import { combineReducers } from 'redux';
import { routerReducer } from 'react-router-redux';
import { reducer as formReducer } from 'redux-form';
import authReducer from './auth';
import dataReducer from './data';
import reportReducer from './report';
import diagnosisReducer from './diagnosis';

export default combineReducers({
    auth: authReducer,
    data: dataReducer,
    report: reportReducer,
    diagnosis: diagnosisReducer,
    routing: routerReducer,
    form: formReducer
});
