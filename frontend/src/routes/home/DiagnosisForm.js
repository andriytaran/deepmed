import React from 'react'
import {createForm} from 'rc-form'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './DiagnosisForm.css'
import {RACES, REGIONS, SITES, TYPES} from '../../constants'
import messages from '../../components/messages'
import {Col, Input, InputNumber, Row, Select} from '../../components'
import Button from 'react-bootstrap/lib/Button'

class DiagnosisForm extends React.Component {
  render() {
    const {onSubmit} = this.props
    const {getFieldDecorator, getFieldError} = this.props.form
    return (
      <form onSubmit={onSubmit} className={s.form}>
        <h3 className={s.header}>Detailed Diagnosis</h3>
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
          </Col>
          <Col xs={24} sm={12} className={s.col}>
            {getFieldDecorator('num_pos_nodes', {
              initialValue: '',
              rules: [
                {required: false, message: messages.required},
              ]
            })(
              <Select error={getFieldError('num_pos_nodes')} label={'Number of Positive Nodes'}>
                <option value='' disabled hidden>Select...</option>
                {Array.from(new Array(24), (val, i) =>
                  <option key={i} value={i}>{i === 23 ? i + '+' : i}</option>
                )}
              </Select>
            )}
          </Col>
        </Row>
        <Row gutter={16}>
          <Col xs={24} sm={12} className={s.col}>
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
          </Col>
          <Col xs={24} sm={12} className={s.col}>
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
          </Col>
        </Row>
        <Row gutter={16}>
          <Col xs={24} sm={12} className={s.col}>
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
          </Col>
          <Col xs={24} sm={12} className={s.col}>
            {getFieldDecorator('ethnicity', {
              initialValue: '',
              rules: [
                {required: true, message: messages.required},
              ]
            })(
              <Select error={getFieldError('ethnicity')} label={'Ethnicity'}>
                <option value='' disabled hidden>Select...</option>
                {RACES.map((item, i) =>
                  <option key={i}>{item}</option>
                )}
              </Select>
            )}
          </Col>
        </Row>
        <Row gutter={16}>
          <Col xs={24} sm={12} className={s.col}>
            {getFieldDecorator('region', {
              initialValue: '',
              rules: [
                {required: false, message: messages.required},
              ]
            })(
              <Select error={getFieldError('region')} label={'Region'}>
                <option value='' disabled hidden>Select...</option>
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
                {required: true, message: messages.required},
              ]
            })(
              <Select error={getFieldError('laterality')} label={'Laterality'}>
                <option value='' disabled hidden>Select...</option>
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
                <option value='' disabled hidden>Select...</option>
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
                {required: true, message: messages.required},
              ]
            })(
              <Select error={getFieldError('type')} label={'Type'}>
                <option value='' disabled hidden>Select...</option>
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
                {required: true, message: messages.required},
              ]
            })(
              <Select error={getFieldError('number_of_tumors')} label={'Number of tumors'}>
                <option value='' disabled hidden>Select...</option>
                {Array.from(new Array(8), (val, i) =>
                  <option key={i} value={i}>{i}</option>
                )}
              </Select>
            )}
          </Col>
        </Row>
        <div className={s.actions}>
          <Button type='submit' bsStyle='primary'>
            Analyze
          </Button>
        </div>
      </form>
    )
  }
}

export default createForm()(withStyles(s)(DiagnosisForm))
