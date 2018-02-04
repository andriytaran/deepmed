import React from 'react'
import {Button} from 'react-bootstrap'
import {createForm} from 'rc-form'
import {RACES} from '../../constants'
import messages from '../../components/messages'
import {Input, Select} from '../../components'

class DiagnosisForm extends React.Component {
  render() {
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
              {getFieldDecorator('age', {
                initialValue: '',
                rules: [
                  {required: true, message: messages.required},
                ]
              })(
                <Input error={getFieldError('age')} label={'Age at Diagnosis'}/>
              )}
            </div>
            <div className="col-xs-6">
              {getFieldDecorator('tumor_size_in_mm', {
                initialValue: '',
                rules: [
                  {required: true, message: messages.required},
                ]
              })(
                <Input error={getFieldError('tumor_size_in_mm')} label={'Tumor Size in mm'}/>
              )}
            </div>
          </div>
          <div className="row push-top-2">
            <div className="col-xs-6">
              {getFieldDecorator('tumor_grade', {
                initialValue: '',
                rules: [
                  {required: true, message: messages.required},
                ]
              })(
                <Select error={getFieldError('tumor_grade')} label={'Tumor Grade'}>
                  <option value='' disabled hidden>Select...</option>
                  <option value={1}>1 (Low)</option>
                  <option value={2}>2 (Medium)</option>
                  <option value={3}>3 (High)</option>
                </Select>
              )}
            </div>
            <div className="col-xs-6">
              {getFieldDecorator('num_pos_nodes', {
                initialValue: '',
                rules: [
                  {required: true, message: messages.required},
                ]
              })(
                <Select error={getFieldError('num_pos_nodes')} label={'Number of Positive Nodes'}>
                  <option value='' disabled hidden>Select...</option>
                  {Array.from(new Array(24), (val, i) =>
                    <option key={i} value={i}>{i}</option>
                  )}
                </Select>
              )}
            </div>
          </div>
          <div className="row push-top-2">
            <div className="col-xs-6">
              {getFieldDecorator('er_status', {
                initialValue: '',
                rules: [
                  {required: true, message: messages.required},
                ]
              })(
                <Select error={getFieldError('er_status')} label={'ER Status'}>
                  <option value='' disabled hidden>Select...</option>
                  <option value='+'>Positive</option>
                  <option value='-'>Negative</option>
                </Select>
              )}
            </div>
            <div className="col-xs-6">
              {getFieldDecorator('her2_status', {
                initialValue: '',
                rules: [
                  {required: true, message: messages.required},
                ]
              })(
                <Select error={getFieldError('her2_status')} label={'HER2 Status'}>
                  <option value='' disabled hidden>Select...</option>
                  <option value='+'>Positive</option>
                  <option value='-'>Negative</option>
                </Select>
              )}
            </div>
          </div>
          <div className="row push-top-2">
            <div className="col-xs-6">
              {getFieldDecorator('pr_status', {
                initialValue: '',
                rules: [
                  {required: true, message: messages.required},
                ]
              })(
                <Select error={getFieldError('pr_status')} label={'PR Status'}>
                  <option value='' disabled hidden>Select...</option>
                  <option value='+'>Positive</option>
                  <option value='-'>Negative</option>
                </Select>
              )}
            </div>
            <div className="col-xs-6">
              {getFieldDecorator('ethnicity', {
                initialValue: '',
                rules: [
                  {required: true, message: messages.required},
                ]
              })(
                <Select error={getFieldError('ethnicity')} label={'Ethnicity'}>
                  <option value='' disabled hidden>Select...</option>
                  {RACES.map((race, i) =>
                    <option key={i}>{race}</option>
                  )}
                </Select>
              )}
            </div>
          </div>
          <div className="row push-top-2">
            <div className="col-xs-6">
              {getFieldDecorator('stage', {
                initialValue: '',
                rules: [
                  {required: true, message: messages.required},
                ]
              })(
                <Select error={getFieldError('stage')} label={'Stage'}>
                  <option value='' disabled hidden>Select...</option>
                  <option value='0'>0</option>
                  <option value='I'>I</option>
                  <option value='II'>II</option>
                  <option value='III'>III</option>
                  <option value='IV'>IV</option>
                </Select>
              )}
            </div>
            <div className="col-xs-6">
              {getFieldDecorator('laterality', {
                initialValue: '',
                rules: [
                  {required: true, message: messages.required},
                ]
              })(
                <Select error={getFieldError('laterality')} label={'Laterality'}>
                  <option value='' disabled hidden>Select...</option>
                  <option value='left'>Left</option>
                  <option value='right'>Right</option>
                </Select>
              )}
            </div>
          </div>
          <div className="row push-top-2">
            <div className="col-xs-6">
              {getFieldDecorator('site', {
                initialValue: '',
                rules: [
                  {required: true, message: messages.required},
                ]
              })(
                <Select error={getFieldError('site')} label={'Site'}>
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
                </Select>
              )}
            </div>
            <div className="col-xs-6">
              {getFieldDecorator('type', {
                initialValue: '',
                rules: [
                  {required: true, message: messages.required},
                ]
              })(
                <Select error={getFieldError('type')} label={'Type'}>
                  <option value='' disabled hidden>Select...</option>
                  <option value='idc'>IDC</option>
                  <option value='ilc'>ILC</option>
                  <option value='dcis'>DCIS</option>
                  <option value='other'>Other</option>
                </Select>
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
