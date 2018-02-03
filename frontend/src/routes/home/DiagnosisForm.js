import React from 'react'
import {Button, FormControl} from 'react-bootstrap'
import {createForm} from 'rc-form'
import {RACES} from '../../constants'

class TextField extends React.Component {
  render() {
    return (
      <div>
        <FormControl type='text' {...this.props}/>
      </div>
    )
  }
}

class SelectField extends React.Component {
  render() {
    const {children, ...otherProps} = this.props
    return (
      <div>
        <select className="form-control" {...otherProps}>
          {children}
        </select>
      </div>
    )
  }
}

class DiagnosisForm extends React.Component {
  render() {
    let errors
    const {onSubmit} = this.props
    const {getFieldDecorator, getFieldError} = this.props.form
    return (
      <form onSubmit={onSubmit}>
        <div className="detailedDiagnosis text-left">
          <div className="row">
            <div className="col-md-12">
              <div className="display-table display-table-100">
                <div className="display-table-cell pad-right-1">
                  <h3 className="no-margin text-light">Detailed Diagnosis</h3>
                </div>
              </div>
            </div>
          </div>
          <div className="row push-top-5">
            <div className="col-xs-6">
              <label>Age at Diagnosis</label>
              {getFieldDecorator('age', {
                initialValue: '',
              })(
                <TextField/>
              )}
            </div>
            <div className="col-xs-6">
              <label>Tumor Size in mm</label>
              {getFieldDecorator('tumor_size_in_mm', {
                initialValue: '',
              })(
                <TextField/>
              )}
            </div>
          </div>
          <div className="row push-top-2">
            <div className="col-xs-6">
              <label>Tumor Grade</label>
              {getFieldDecorator('tumor_grade', {
                initialValue: '',
              })(
                <SelectField>
                  <option value='' disabled hidden>Select...</option>
                  <option value={1}>1 (Low)</option>
                  <option value={2}>2 (Medium)</option>
                  <option value={3}>3 (High)</option>
                </SelectField>
              )}
            </div>
            <div className="col-xs-6">
              <label><span className="hidden-xs">Number</span><span
                className="visible-xs display-inline">#</span> of Positive Nodes</label>
              {getFieldDecorator('num_pos_nodes', {
                initialValue: '',
              })(
                <SelectField>
                  <option value='' disabled hidden>Select...</option>
                  {Array.from(new Array(24), (val, i) =>
                    <option key={i} value={i}>{i}</option>
                  )}
                </SelectField>
              )}
            </div>
          </div>
          <div className="row push-top-2">
            <div className="col-xs-6">
              <label>ER Status</label>
              {getFieldDecorator('er_status', {
                initialValue: '',
              })(
                <SelectField>
                  <option value='' disabled hidden>Select...</option>
                  <option value='+'>Positive</option>
                  <option value='-'>Negative</option>
                </SelectField>
              )}
            </div>
            <div className="col-xs-6">
              <label>HER2 Status</label>
              {getFieldDecorator('her2_status', {
                initialValue: '',
              })(
                <SelectField>
                  <option value='' disabled hidden>Select...</option>
                  <option value='+'>Positive</option>
                  <option value='-'>Negative</option>
                </SelectField>
              )}
            </div>
          </div>
          <div className="row push-top-2">
            <div className="col-xs-6">
              <label>PR Status</label>
              {getFieldDecorator('pr_status', {
                initialValue: '',
              })(
                <SelectField>
                  <option value='' disabled hidden>Select...</option>
                  <option value='+'>Positive</option>
                  <option value='-'>Negative</option>
                </SelectField>
              )}
            </div>
            <div className="col-xs-6">
              <label>Ethnicity (optional)</label>
              {getFieldDecorator('ethnicity', {
                initialValue: '',
              })(
                <SelectField>
                  <option value='' disabled hidden>Select...</option>
                  {RACES.map((race, i) =>
                    <option key={i}>{race}</option>
                  )}
                </SelectField>
              )}
            </div>
          </div>
          <div className="row push-top-2">
            <div className="col-xs-6">
              <label>Stage</label>
              {getFieldDecorator('stage', {
                initialValue: '',
              })(
                <SelectField>
                  <option value='' disabled hidden>Select...</option>
                  <option value='0'>0</option>
                  <option value='I'>I</option>
                  <option value='II'>II</option>
                  <option value='III'>III</option>
                  <option value='IV'>IV</option>
                </SelectField>
              )}
            </div>
            <div className="col-xs-6">
              <label>Laterality</label>
              {getFieldDecorator('laterality', {
                initialValue: '',
              })(
                <SelectField>
                  <option value='' disabled hidden>Select...</option>
                  <option value='left'>Left</option>
                  <option value='right'>Right</option>
                </SelectField>
              )}
            </div>
          </div>
          <div className="row push-top-2">
            <div className="col-xs-6">
              <label>Stage</label>
              {getFieldDecorator('site', {
                initialValue: '',
              })(
                <SelectField>
                  <option value='' disabled hidden>Select...</option>
                  <option value='nipple'>Nipple</option>
                  <option value='center'>Center</option>
                  <option value='upper_inner'>Upper-Inner</option>
                  <option value='lower_inner'>Lower-Inner</option>
                  <option value='upper_outer'>Upper-Outer</option>
                  <option value='lower_outer'>Lower-Outer</option>
                  <option value='axillary'>Axillary</option>
                  <option value='overlapping'>Overlapping</option>
                  <option value='nos'>NoS</option>
                </SelectField>
              )}
            </div>
            <div className="col-xs-6">
              <label>Laterality</label>
              {getFieldDecorator('type', {
                initialValue: '',
              })(
                <SelectField>
                  <option value='' disabled hidden>Select...</option>
                  <option value='idc'>IDC</option>
                  <option value='ilc'>ILC</option>
                  <option value='dcis'>DCIS</option>
                  <option value='other'>Other</option>
                </SelectField>
              )}
            </div>
          </div>
          <div className="row push-top-2">
            <div className="col-xs-12 text-center position-relative">
              <Button bsSize="large" bsStyle="primary" type="submit" className="btn-offset">
                Analyze
              </Button>
            </div>
          </div>
        </div>
      </form>
    )
  }
}

export default createForm()(DiagnosisForm)
