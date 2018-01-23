import React from 'react';
import {Field, reduxForm} from 'redux-form';

import {Button, FormControl} from 'react-bootstrap';
import Link from '../../components/Link';

const SearchField = ({input, label, type, meta: {touched, error}}) => (
    <div>
        <FormControl type="text" className="text-input-lg" bsSize="large"/>
        {touched && error && <span>{error}</span>}
    </div>
);

const TextField = ({input, label, type, meta: {touched, error}}) => (
    <div>
        <FormControl type="text"/>
        {touched && error && <span>{error}</span>}
    </div>
);

const SelectField = (
    {
        input,
        label,
        meta: {touched, error},
        children
    }) => (
    <div>
        <label>{label}</label>
        <div className={touched ? (error ? 'error' : 'success') : ''}>
            <select {...input} className="form-control">
                {children}
            </select>
            {touched && (error && <p className="help error">{error}</p>)}
        </div>
    </div>
);

const DiagnosisForm = props => {
    const {handleSubmit, pristine, reset, submitting, showDetails, onShowDetails} = props
    return (
        <form onSubmit={handleSubmit}>

            { !showDetails &&
            <div className="simpleSearch">
                <div className="row">
                    <div className="col-md-12">
                        <div className="display-table display-table-100">
                            <div className="display-table-cell pad-right-1">
                                <Field name="conditions"
                                    component={SearchField}
                                    type="text" />
                            </div>
                            <div className="display-table-cell text-right" style={{width: 145}}>
                                <Button bsSize="large" bsStyle="primary" block type="submit">
                                    Analyze
                                </Button>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="row push-top-2">
                    <div className="col-md-12">
                        <Link onClick={() => {
                            onShowDetails(true);
                        }}>
                            Input Detailed Diagnosis
                        </Link>
                    </div>
                </div>
            </div>}

            { showDetails &&
            <div className="detailedDiagnosis text-left">
                <div className="row">
                    <div className="col-md-12">
                        <div className="display-table display-table-100">
                            <div className="display-table-cell pad-right-1">
                                <h3 className="no-margin text-light">Detailed Diagnosis</h3>
                            </div>
                            <div className="display-table-cell pad-left-1 text-right">
                                <Link onClick={() => {
                                    onShowDetails(false);
                                }}>
                                    <i className="fa fa-arrow-left"/>
                                    &nbsp;Back to basic diagnosis entry
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="row push-top-5">
                    <div className="col-xs-6">
                        <label>Age at Diagnosis</label>
                        <Field name="age" component={TextField} />
                    </div>
                    <div className="col-xs-6">
                        <label>Tumor Size in mm</label>
                        <Field name="tumor_size" component={TextField} />
                    </div>
                </div>
                <div className="row push-top-2">
                    <div className="col-xs-6">
                        <label>Tumor Grade</label>
                        <Field name="tumor_grade"
                            component={SelectField}>
                            <option>1 (Low)</option>
                            <option>2 (Medium)</option>
                            <option>3 (High)</option>
                        </Field>
                    </div>
                    <div className="col-xs-6">
                        <label><span className="hidden-xs">Number</span><span
                            className="visible-xs display-inline">#</span> of Positive Nodes</label>
                        <Field name="positive_nodes" component={SelectField}>
                            {Array.from(new Array(24), (val, index) => { return <option key={index} value={index + 1}>{index + 1}</option>; })}
                        </Field>
                    </div>
                </div>
                <div className="row push-top-2">
                    <div className="col-xs-6">
                        <label>ER Status</label>
                        <Field name="er_status" component={SelectField}>
                            <option>Positive</option>
                            <option>Negative</option>
                        </Field>
                    </div>
                    <div className="col-xs-6">
                        <label>HER2 Status</label>
                        <Field name="her2_status" component={SelectField}>
                            <option>Positive</option>
                            <option>Negative</option>
                        </Field>
                    </div>
                </div>
                <div className="row push-top-2">
                    <div className="col-xs-6">
                        <label>PR Status</label>
                        <Field name="pr_status" component={SelectField}>
                            <option>Positive</option>
                            <option>Negative</option>
                        </Field>
                    </div>
                    <div className="col-xs-6">
                        <label>Ethnicity (optional)</label>
                        <Field name="ethnicity" component={SelectField}>
                            <option>African-American</option>
                            <option>Asian</option>
                            <option>Native American</option>
                            <option>Caucasian</option>
                        </Field>
                    </div>
                </div>
                <div className="row push-top-2">
                    <div className="col-xs-12 text-center position-relative">
                        <Button bsSize="large" bsStyle="primary" type="submit" className="btn-offset">
                            &nbsp;&nbsp;&nbsp;Analyze&nbsp;&nbsp;&nbsp;
                        </Button>
                    </div>
                </div>
            </div>}

        </form>
    );
};

export default reduxForm({
    form: 'diagnosis'
})(DiagnosisForm);
