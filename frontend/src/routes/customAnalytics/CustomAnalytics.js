import React from 'react'
import {connect} from 'react-redux'
import {createForm} from 'rc-form'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './CustomAnalytics.scss'
import {Row, Col, Select, Card} from '../../components'
import {RACES, AGES, TYPES} from '../../constants'
import {getCustomAnalytics} from '../../reducers/diagnosis'
import messages from '../../components/messages'
import pickBy from 'lodash/pickBy'
import identity from 'lodash/identity'
import isEmpty from 'lodash/isEmpty'
import {Pie} from 'react-chartjs-2'
import {formatChartNumber} from '../../utils'

class CustomAnalytics extends React.Component {
  state = {
    fields: {}
  }

  changeField = (value, key) => {
    this.setState({
      fields: {
        ...this.state.fields,
        [key]: value,
      }
    })
  }

  handleSubmit = (e) => {
    e.preventDefault()
    this.props.form.validateFields((err, values) => {
      if (!err) {
        this.props.getCustomAnalytics({
          ...values,
          // remove empty filters because of native select field default options
          filters: pickBy(values.filters, identity)
        })
      }
    })
  }

  clearFilters = () => {
    this.props.form.resetFields()
  }

  render() {
    // TODO move it to constants
    const white = '#fff'
    const color_1 = '#48ccf5'
    const color_2 = '#88d0d1'
    const color_3 = '#47cfd1'
    const color_4 = '#b8e8f5'
    const color_5 = '#1ac6ff'
    const color_6 = '#8f61ec'
    const color_7 = '#9df51d'
    const color_8 = '#ff9400'
    const color_9 = '#f51431'

    const chartsLabelsOptions = {
      boxWidth: 10,
      fontSize: 10,
      padding: 8
    }
    const {fields} = this.state
    const {customAnalytics, customAnalyticsLoading} = this.props
    const {getFieldDecorator, getFieldError} = this.props.form

    return (
      <form onSubmit={this.handleSubmit} className='container container-full'>
        <Row type='flex' gutter={16}>
          <Col xs={24} md={6}>
            <div className={s.filter}>
              {getFieldDecorator('filters[age]', {
                initialValue: '',
              })(
                <Select className={s.field} error={getFieldError('filters[age]')} label={'Age'}>
                  <option value='' disabled hidden>Select...</option>
                  {AGES.map((item, i) =>
                    <option key={i} value={item.value}>{item.label}</option>
                  )}
                </Select>
              )}
            </div>
            <div className={s.filter}>
              {getFieldDecorator('filters[ethnicity]', {
                initialValue: '',
              })(
                <Select
                  onChange={(e) => this.changeField(e.target.value, 'ethnicity')}
                  className={s.field}
                  error={getFieldError('filters[ethnicity]')}
                  label={'Ethnicity'}
                >
                  <option value='' disabled hidden>Select...</option>
                  {RACES.map((item, i) =>
                    <option key={i}>{item}</option>
                  )}
                </Select>
              )}
            </div>
            <div className={s.filter}>
              {getFieldDecorator('filters[tumor_grade]', {
                initialValue: '',
              })(
                <Select
                  onChange={(e) => this.changeField(e.target.value, 'grade')}
                  className={s.field}
                  error={getFieldError('filters[tumor_grade]')}
                  label={'Tumor Grade'}
                >
                  <option value='' disabled hidden>Select...</option>
                  <option value={1}>1 (Low)</option>
                  <option value={2}>2 (Medium)</option>
                  <option value={3}>3 (High)</option>
                </Select>
              )}
            </div>
            <div className={s.filter}>
              {getFieldDecorator('filters[num_pos_nodes]', {
                initialValue: '',
              })(
                <Select className={s.field} error={getFieldError('filters[num_pos_nodes]')} label={'Number of Positive Nodes'}>
                  <option value='' disabled hidden>Select...</option>
                  {Array.from(new Array(24), (val, i) =>
                    <option key={i} value={i}>{i === 23 ? i + '+' : i}</option>
                  )}
                </Select>
              )}
            </div>
            <div className={s.filter}>
              {getFieldDecorator('filters[er_status]', {
                initialValue: '',
              })(
                <Select className={s.field} error={getFieldError('filters[er_status]')} label={'ER Status'}>
                  <option value='' disabled hidden>Select...</option>
                  <option value='+'>Positive</option>
                  <option value='-'>Negative</option>
                </Select>
              )}
            </div>
            <div className={s.filter}>
              {getFieldDecorator('filters[pr_status]', {
                initialValue: '',
              })(
                <Select className={s.field} error={getFieldError('filters[pr_status]')} label={'PR Status'}>
                  <option value='' disabled hidden>Select...</option>
                  <option value='+'>Positive</option>
                  <option value='-'>Negative</option>
                </Select>
              )}
            </div>
            <div className={s.filter}>
              {getFieldDecorator('filters[her2_status]', {
                initialValue: '',
              })(
                <Select className={s.field} error={getFieldError('filters[her2_status]')} label={'HER2 Status'}>
                  <option value='' disabled hidden>Select...</option>
                  <option value='+'>Positive</option>
                  <option value='-'>Negative</option>
                </Select>
              )}
            </div>
            <div className={s.filter}>
              {getFieldDecorator('filters[type]', {
                initialValue: '',
              })(
                <Select
                  onChange={(e) => this.changeField(e.target.value, 'type')}
                  className={s.field}
                  error={getFieldError('filters[type]')}
                  label={'Type'}
                >
                  <option value='' disabled hidden>Select...</option>
                  {TYPES.map((item, i) =>
                    <option key={i} value={item.value}>{item.label}</option>
                  )}
                </Select>
              )}
            </div>
            <div className={s.filter}>
              {getFieldDecorator('filters[number_of_tumors]', {
                initialValue: '',
              })(
                <Select className={s.field} error={getFieldError('filters[number_of_tumors]')} label={'Number of tumors'}>
                  <option value='' disabled hidden>Select...</option>
                  {Array.from(new Array(8), (val, i) =>
                    <option key={i} value={i}>{i}</option>
                  )}
                </Select>
              )}
            </div>
            <div className={s.submitBtnWrapper}>
              <button className='btn btn-primary' type='submit'>Submit</button>
            </div>
          </Col>
          <Col xs={24} md={16} className={s.chartColumn}>
            <div className={s.groupWrapper}>
              {getFieldDecorator('group', {
                initialValue: '',
                rules: [
                  {required: true, message: messages.required},
                ]
              })(
                <Select className={s.field} error={getFieldError('group')} label={'Group by'}>
                  <option value='' disabled hidden>Select...</option>
                  <option value={'grade'} disabled={fields.grade}>Tumor Grade</option>
                  <option value={'stage'}>Stage</option>
                  <option value={'type'} disabled={fields.type}>Type</option>
                  <option value={'ethnicity'} disabled={fields.ethnicity}>Ethnicity</option>
                  <option value={'cod'}>Cause of Death</option>
                  <option value={'radiation'}>Radiation</option>
                  <option value={'chemo'}>Chemotherapy</option>
                  <option value={'surgery'}>Surgery</option>
                </Select>
              )}
              <a
                className={s.clearFiltersBtn}
                onClick={this.clearFilters}
              >
                Clear filters
              </a>
            </div>
            <div className={s.chartWrapper}>
              <Card
                className={s.chartCard}
                loading={customAnalyticsLoading}
              >
                {!isEmpty(customAnalytics.custom_analytics) && (
                  <Pie
                    data={{
                      ...customAnalytics.custom_analytics,
                      datasets: customAnalytics.custom_analytics.datasets.map(item => ({
                        ...item,
                        backgroundColor: [color_1, color_3, color_4, color_2, color_5, color_6, color_7, color_8, color_9],
                        borderColor: white,
                      }))
                    }}
                    options={{
                      legend: {
                        display: true,
                        position: 'bottom',
                        labels: chartsLabelsOptions
                      },
                      tooltips: {
                        callbacks: {
                          label: formatChartNumber
                        }
                      },
                    }}
                    width={400}
                    height={200}
                  />
                )}
              </Card>
            </div>
          </Col>
        </Row>
      </form>
    )
  }
}

const mapState = state => ({
  ...state.diagnosis,
})

const mapDispatch = {
  getCustomAnalytics,
}

export default connect(mapState, mapDispatch)(createForm()(withStyles(s)(CustomAnalytics)))
