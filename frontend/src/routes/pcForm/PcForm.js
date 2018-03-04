import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import {createForm} from 'rc-form'
// import {getData} from '../../reducers/breastCancer'
import s from './PcForm.css'
import {RACES, REGIONS, SITES, STAGES, TUMOR_GRADES, TYPES} from '../../constants'
import messages from '../../components/messages'
import {Col, Input, InputNumber, Row, Select, Link} from '../../components/index'
import Button from 'react-bootstrap/lib/Button'
import {HOME_ROUTE} from '../index'

class PcForm extends React.Component {
  state = {
    expanded: false,
  }

  expand = () => {
    this.setState({ expanded: !this.state.expanded })
  }

  handleSubmit = (e) => {
    e.preventDefault()
    this.props.form.validateFields((err, values) => {
      if (!err) {
        // this.props.getData(values)
      }
    })
  }

  render() {
    const {expanded} = this.state
    const {getFieldDecorator, getFieldError} = this.props.form
    return (
      <div className={s.container}>
        <Link to={HOME_ROUTE}>
          <div className={s.back}>
            Back
          </div>
        </Link>
        <h2 className={s.header}>
          Please input your diagnosis in detail below
        </h2>
        <form onSubmit={this.handleSubmit} className={s.form}>
          <h3 className={s.formHeader}>Detailed Diagnosis</h3>
          <Row gutter={16}>
            <Col xs={24} sm={12} className={s.col}>
              {getFieldDecorator('age', {
                initialValue: '',
                rules: [
                  {required: true, message: messages.required},
                  {min: 18, message: messages.minAge, type: 'number'},
                ],
              })(
                <InputNumber error={getFieldError('age')} label={'Age at Diagnosis'}/>
              )}
            </Col>
            <Col xs={24} sm={12} className={s.col}>
              {getFieldDecorator('tumor_size_in_mm', {
                initialValue: '',
                rules: [
                  {required: false, message: messages.required},
                ]
              })(
                <Input error={getFieldError('tumor_size_in_mm')} label={'Tumor Size in mm'}/>
              )}
            </Col>
          </Row>
          <Row gutter={16}>
            <Col xs={24} sm={12} className={s.col}>
              {getFieldDecorator('gleason-pri', {
                initialValue: '',
                rules: [
                  {required: false, message: messages.required},
                ]
              })(
                <Input error={getFieldError('gleason-pri')} label={'Gleason primRy score'}/>
              )}
            </Col>
            <Col xs={24} sm={12} className={s.col}>
              {getFieldDecorator('gleason-sec', {
                initialValue: '',
                rules: [
                  {required: false, message: messages.required},
                ]
              })(
                <Input error={getFieldError('gleason-sec')} label={'Gleason secondary score'}/>
              )}
            </Col>
          </Row>
          <Row gutter={16}>
            <Col xs={24} sm={12} className={s.col}>
              {getFieldDecorator('ethnicity', {
                initialValue: '',
                rules: [
                  {required: false, message: messages.required},
                ]
              })(
                <Select error={getFieldError('ethnicity')} label={'Ethnicity'}>
                  <option value=''>Select...</option>
                  {RACES.map((item, i) =>
                    <option key={i}>{item}</option>
                  )}
                </Select>
              )}
            </Col>
            <Col xs={24} sm={12} className={s.col}>
              {getFieldDecorator('psa', {
                initialValue: '',
                rules: [
                  {required: false, message: messages.required},
                ]
              })(
                <Input error={getFieldError('psa')} label={'PSA'}/>
              )}
            </Col>
          </Row>
          {/*hidden fields should be sent*/}
          <div style={{display: expanded ? 'block' : 'none'}}>
            <Row gutter={16}>
              <Col xs={24} sm={12} className={s.col}>
                {getFieldDecorator('region', {
                  initialValue: '',
                  rules: [
                    {required: false, message: messages.required},
                  ]
                })(
                  <Select error={getFieldError('region')} label={'Region'}>
                    <option value=''>Select...</option>
                    {REGIONS.map((item, i) =>
                      <option key={i} value={item.value}>{item.label}</option>
                    )}
                  </Select>
                )}
              </Col>
              <Col xs={24} sm={12} className={s.col}>
                {getFieldDecorator('laterality', {
                  initialValue: '',
                  rules: [
                    {required: false, message: messages.required},
                  ]
                })(
                  <Select error={getFieldError('laterality')} label={'Laterality'}>
                    <option value=''>Select...</option>
                    <option value='left'>Left</option>
                    <option value='right'>Right</option>
                  </Select>
                )}
              </Col>
            </Row>
            <Row gutter={16}>
              <Col xs={24} sm={12} className={s.col}>
                {getFieldDecorator('site', {
                  initialValue: '',
                  rules: [
                    {required: false, message: messages.required},
                  ]
                })(
                  <Select error={getFieldError('site')} label={'Site'}>
                    <option value=''>Select...</option>
                    {SITES.map((item, i) =>
                      <option key={i} value={item.value}>{item.label}</option>
                    )}
                  </Select>
                )}
              </Col>
              <Col xs={24} sm={12} className={s.col}>
                {getFieldDecorator('type', {
                  initialValue: '',
                  rules: [
                    {required: false, message: messages.required},
                  ]
                })(
                  <Select error={getFieldError('type')} label={'Type'}>
                    <option value=''>Select...</option>
                    {TYPES.map((item, i) =>
                      <option key={i} value={item.value}>{item.label}</option>
                    )}
                  </Select>
                )}
              </Col>
            </Row>
            <Row gutter={16}>
              <Col xs={24} sm={12} className={s.col}>
                {getFieldDecorator('number_of_tumors', {
                  initialValue: '',
                  rules: [
                    {required: false, message: messages.required},
                  ]
                })(
                  <Select error={getFieldError('number_of_tumors')} label={'Number of tumors'}>
                    <option value=''>Select...</option>
                    {Array.from(new Array(7), (val, i) =>
                      <option key={i} value={i+1}>{i+1}</option>
                    )}
                  </Select>
                )}
              </Col>
              <Col xs={24} sm={12} className={s.col}>
                {getFieldDecorator('stage', {
                  initialValue: '',
                  rules: [
                    {required: false, message: messages.required},
                  ]
                })(
                  <Select error={getFieldError('stage')} label={'Stage'}>
                    <option value=''>Select...</option>
                    {STAGES.map((item, i) =>
                      <option key={i} value={item.value}>{item.label}</option>
                    )}
                  </Select>
                )}
              </Col>
            </Row>
          </div>
          {!expanded && (
            <div className={s.advancedDetailsBtnWrapper}>
              <a onClick={this.expand} className={s.advancedDetailsBtn}>Advanced Details</a>
            </div>
          )}
          <div className={s.actions}>
            <Button type='submit' bsStyle='primary'>
              Analyze
            </Button>
          </div>
        </form>
      </div>
    )
  }
}

const mapState = state => ({
  ...state.prostateCancer,
})

const mapDispatch = {
  // getData,
}

export default connect(mapState, mapDispatch)(createForm()(withStyles(s)(PcForm)))
