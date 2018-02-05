import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './Diagnosis.scss'
import {RACES} from '../../constants'
import {createForm} from 'rc-form'
import messages from '../../components/messages'
import {Input, Select} from '../../components'
import isEmpty from 'lodash/isEmpty'
import {Button} from 'react-bootstrap'
import {getDiagnosisData} from '../../reducers/diagnosis'

class Diagnosis extends React.Component {
  handleSubmit = (e) => {
    e.preventDefault()
    this.props.form.validateFields((err, values) => {
      if (!err) {
        this.props.getDiagnosisData(values)
      }
    })
  }

  render() {
    const {data, diagnosisForm} = this.props
    const {getFieldDecorator, getFieldError} = this.props.form
    return (
      <div className='container container-full'>
        <div className='row'>
          <div className='col-md-12'>
            {!isEmpty(diagnosisForm) && (
              <div className='custom-panel custom-panel-condensed light-gray-bg'>
                <h2 className='push-top-2'>Diagnosis</h2>
                <form onSubmit={this.handleSubmit}>
                  <div className='row row-condensed push-top-2-xs'>
                    <div className='col-sm-2 col-xs-6'>
                      {getFieldDecorator('age', {
                        initialValue: diagnosisForm.age,
                        rules: [
                          {required: true, message: messages.required},
                        ]
                      })(
                        <Input error={getFieldError('age')} label={'Age at Diagnosis'}/>
                      )}
                    </div>
                    <div className='col-sm-2 col-xs-6'>
                      {getFieldDecorator('tumor_size_in_mm', {
                        initialValue: diagnosisForm.tumor_size_in_mm,
                        rules: [
                          {required: true, message: messages.required},
                        ]
                      })(
                        <Input error={getFieldError('tumor_size_in_mm')} label={'Tumor Size in mm'}/>
                      )}
                    </div>
                    <div className='col-sm-2 col-xs-6 push-top-2-xs'>
                      {getFieldDecorator('tumor_grade', {
                        initialValue: diagnosisForm.tumor_grade,
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
                    <div className='col-sm-2 col-xs-6 push-top-2-xs'>
                      {getFieldDecorator('num_pos_nodes', {
                        initialValue: diagnosisForm.num_pos_nodes,
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
                    <div className='col-sm-2 col-xs-6 push-top-2-xs'>
                      {getFieldDecorator('er_status', {
                        initialValue: diagnosisForm.er_status,
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
                    <div className='col-sm-2 col-xs-6 push-top-2-xs'>
                      {getFieldDecorator('her2_status', {
                        initialValue: diagnosisForm.her2_status,
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
                  <div className='row row-condensed push-top-2-xs'>
                    <div className='col-sm-2 col-xs-6'>
                      {getFieldDecorator('pr_status', {
                        initialValue: diagnosisForm.pr_status,
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
                    <div className='col-sm-2 col-xs-6'>
                      {getFieldDecorator('ethnicity', {
                        initialValue: diagnosisForm.ethnicity,
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
                    <div className='col-sm-2 col-xs-6 push-top-2-xs'>
                      {getFieldDecorator('stage', {
                        initialValue: diagnosisForm.stage,
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
                    <div className='col-sm-2 col-xs-6 push-top-2-xs'>
                      {getFieldDecorator('site', {
                        initialValue: diagnosisForm.site,
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
                    <div className='col-sm-2 col-xs-6 push-top-2-xs'>
                      {getFieldDecorator('laterality', {
                        initialValue: diagnosisForm.laterality,
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
                    <div className='col-sm-2 col-xs-6 push-top-2-xs'>
                      {getFieldDecorator('type', {
                        initialValue: diagnosisForm.type,
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
                  <div className="row row-condensed push-top-2-xs">
                    <div className="col-xs-12 text-center position-relative">
                      <Button bsSize="large" bsStyle="primary" type="submit" className={s.analyzeBtn}>
                        Analyze
                      </Button>
                    </div>
                  </div>
                </form>
              </div>
            )}
            <div className='custom-panel custom-panel-condensed light-gray-bg push-bot-0'>
              <h2 className='push-top-2'>Recommended Treatment Plans</h2>
              {data.recommended_treatment_plans && data.recommended_treatment_plans.overall_plans && (
                <div className='push-top-5'>
                  <div
                    className='custom-panel custom-panel-condensed custom-panel-no-vertical-pad no-border bg-transparent push-bot-0'>
                    <p className='push-top-0 push-bot-1'><strong>Overall Plans</strong></p>
                  </div>
                  <div className='custom-panel custom-panel-condensed push-bot-0'>
                    <table
                      className='table table-responsive table-middle-cell-align table-hover tablesaw tablesaw-stack'
                      data-tablesaw-mode='stack'>
                      <thead>
                      <tr>
                        <th><h6>TREATMENT PLANS</h6></th>
                        <th><h6>CONFIDENCE LEVEL</h6></th>
                        <th><h6>SURGERY</h6></th>
                        <th><h6>SURGERY TYPE</h6></th>
                        <th><h6>RADIATION</h6></th>
                        <th><h6>CHEMO</h6></th>
                      </tr>
                      </thead>
                      <tbody>
                      {data.recommended_treatment_plans.overall_plans.map((item, i) =>
                        <tr key={i}>
                          <td><p className="no-margin">Preferred Outcome A</p></td>
                          <td><p className="no-margin">{item['level']}%</p></td>
                          <td><p className="no-margin">{item['surgery']}</p></td>
                          <td><p className="no-margin">{item['type']}</p></td>
                          <td><p className="no-margin">{item['radiation']}</p></td>
                          <td><p className="no-margin">{item['chemo']}</p></td>
                        </tr>
                      )}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
              <div className='push-top-5'>
                <div
                  className='custom-panel custom-panel-condensed custom-panel-no-vertical-pad no-border bg-transparent push-bot-0'>
                  <p className='push-top-0 push-bot-1'><strong>Chemotherapy</strong></p>
                </div>
                <div className='custom-panel custom-panel-condensed push-bot-0'>
                  <table
                    className='table table-responsive table-middle-cell-align table-equal-width-3 table-hover tablesaw tablesaw-stack'
                    data-tablesaw-mode='stack'>
                    <thead>
                    <tr>
                      <th><h6>CHEMO TREATMENT PLANS</h6></th>
                      <th><h6>NUMBER OF TREATMENTS</h6></th>
                      <th><h6>ADMINISTRATION</h6></th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                      <td><p className='no-margin'><span
                        className='number-circle blue-circle'>1</span> AC + T</p></td>
                      <td>
                        <table>
                          <tr>
                            <td>
                              <p className='push-bot-1 push-top-1'>A) 4AC, 4T</p>
                            </td>
                          </tr>
                          <tr>
                            <td>
                              <p className='push-bot-1 push-top-1'>B) 4AC, 12T</p>
                            </td>
                          </tr>
                        </table>
                      </td>
                      <td>
                        <table>
                          <tr>
                            <td>
                              <p className='no-margin'>A)</p>
                            </td>
                            <td className='pad-left-1 pad-right-1'>
                              <p className='no-margin'>AC</p>
                              <p className='push-bot-1 line-height-condensed small'>
                                <small>Every 2 weeks</small>
                              </p>
                            </td>
                            <td className='vertical-line'></td>
                            <td className='pad-left-2'>
                              <p className='no-margin'>T</p>
                              <p className='push-bot-1 line-height-condensed small'>
                                <small>Every 2 weeks</small>
                              </p>
                            </td>
                          </tr>
                          <tr>
                            <td>
                              <p className='no-margin'>B)</p>
                            </td>
                            <td className='pad-left-1 pad-right-1'>
                              <p className='push-top-1'>AC</p>
                              <p className='no-margin line-height-condensed small'>
                                <small>Every 2 weeks</small>
                              </p>
                            </td>
                            <td className='vertical-line'></td>
                            <td className='pad-left-2'>
                              <p className='push-top-1'>T</p>
                              <p className='no-margin line-height-condensed small'>
                                <small>Every week</small>
                              </p>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                    <tr>
                      <td><p className='no-margin'><span
                        className='number-circle blue-circle'>2</span> FEC</p></td>
                      <td><p className='no-margin'>3 FEC</p></td>
                      <td><p className='no-margin'>Every 3 weeks</p></td>
                    </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <div className='push-top-5'>
                <div
                  className='custom-panel custom-panel-condensed custom-panel-no-vertical-pad no-border bg-transparent push-bot-0'>
                  <p className='push-top-0 push-bot-1'><strong>Radiation Therapy</strong></p>
                </div>
                <div className='custom-panel custom-panel-condensed push-bot-0'>
                  <table
                    className='table table-responsive table-middle-cell-align table-equal-width-3 table-hover tablesaw tablesaw-stack'
                    data-tablesaw-mode='stack'>
                    <thead>
                    <tr>
                      <th><h6>RADIATION TREATMENT PLANS</h6></th>
                      <th><h6>NUMBER OF TREATMENTS</h6></th>
                      <th><h6>ADMINISTRATION</h6></th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                      <td><p className='no-margin'><span
                        className='number-circle blue-circle'>1</span> Beam Radiation</p></td>
                      <td><p className='no-margin'>30</p></td>
                      <td><p className='no-margin'>Daily</p></td>
                    </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <div className='push-top-5'>
                <div
                  className='custom-panel custom-panel-condensed custom-panel-no-vertical-pad no-border bg-transparent push-bot-0'>
                  <p className='push-top-0 push-bot-1'><strong>Hormonal Therapy</strong></p>
                </div>
                <div className='custom-panel custom-panel-condensed push-bot-0'>
                  <table
                    className='table table-responsive table-middle-cell-align table-equal-width-3 table-hover tablesaw tablesaw-stack'
                    data-tablesaw-mode='stack'>
                    <thead>
                    <tr>
                      <th><h6>HORMONAL TREATMENT PLANS</h6></th>
                      <th><h6>NUMBER OF TREATMENTS</h6></th>
                      <th><h6>ADMINISTRATION</h6></th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                      <td><p className='no-margin'><span
                        className='number-circle blue-circle'>1</span> Tamoxifen</p></td>
                      <td><p className='no-margin'>120</p></td>
                      <td><p className='no-margin'>Monthly</p></td>
                    </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

const mapState = state => ({
  ...state.diagnosis,
})

const mapDispatch = {
  getDiagnosisData,
}

export default connect(mapState, mapDispatch)(createForm()(withStyles(s)(Diagnosis)))
