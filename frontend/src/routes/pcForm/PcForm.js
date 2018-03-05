import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import {createForm} from 'rc-form'
import {getData} from '../../reducers/prostateCancer'
import s from './PcForm.css'
import {RACES_FOR_PROSTATE, REGIONS, SITES, STAGES, TUMOR_GRADES, TYPES} from '../../constants'
import messages from '../../components/messages'
import {Col, Input, InputNumber, Row, Select, Link} from '../../components/index'
import Button from 'react-bootstrap/lib/Button'
import {HOME_ROUTE} from '../index'

class PcForm extends React.Component {

  handleSubmit = (e) => {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        this.props.getData(values)
      }
    })
  };

  render() {
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
              {getFieldDecorator('gleason_primary', {
                initialValue: '',
                rules: [
                  {required: false, message: messages.required},
                ]
              })(
                <Input error={getFieldError('gleason_primary')} label={'Gleason primary score'}/>
              )}
            </Col>
            <Col xs={24} sm={12} className={s.col}>
              {getFieldDecorator('gleason_secondary', {
                initialValue: '',
                rules: [
                  {required: false, message: messages.required},
                ]
              })(
                <Input error={getFieldError('gleason_secondary')} label={'Gleason secondary score'}/>
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
                  {RACES_FOR_PROSTATE.map((item, i) =>
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
});

const mapDispatch = {
  getData,
};

export default connect(mapState, mapDispatch)(createForm()(withStyles(s)(PcForm)))
