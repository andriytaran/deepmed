import React from 'react'
import {connect} from 'react-redux'
import {createForm} from 'rc-form'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './BcSurvivalMonths.css'
import {Row, Col, Select, Card} from '../../components'
import {
  AGES, TYPES, TUMOR_SIZES, SITES, NUMBER_OF_NODES, GROUPED_RACES, NUMBER_OF_TUMORS,
  STAGES, TUMOR_GRADES, GROUPED_SURVIVAL_MONTHS
} from '../../constants'
import {getCustomAnalytics} from '../../reducers/breastCancer'
import messages from '../../components/messages'
import pickBy from 'lodash/pickBy'
import identity from 'lodash/identity'
import isEmpty from 'lodash/isEmpty'
import {Bar} from 'react-chartjs-2'
import {formatChartNumber} from '../../utils'
import Button from 'react-bootstrap/lib/Button'
import isNil from 'lodash/isNil'


class BcSurvivalMonths extends React.Component {
  state = {
    fields: {},
  }

  changeField = (value, key) => {
    this.setState({
      fields: {
        ...this.state.fields,
        [key]: value,
      }
    })

  }

  handleSubmit = (title) => event => {
    event.preventDefault()
    this.props.form.validateFields((err, values) => {
      if (!err) {
        values.ca_type = title
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
    this.setState({fields: {}})
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
      <form onSubmit={this.handleSubmit('survival_months')} className={s.container}>
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
                  {GROUPED_RACES.map((race, i) =>
                    race.label ? (
                      <optgroup key={i} label={race.label}>
                        {race.values.map((item, j) =>
                          <option key={j}>{item}</option>
                        )}
                      </optgroup>
                    ) : (
                      <option key={i}>{race}</option>
                    )
                  )}
                </Select>
              )}
            </div>
            <div className={s.filter}>
              {getFieldDecorator('filters[tumor_size]', {
                initialValue: '',
              })(
                <Select
                  onChange={(e) => this.changeField(e.target.value, 'tumor_size')}
                  className={s.field}
                  error={getFieldError('filters[tumor_size]')}
                  label={'Tumor Size'}>
                  <option value='' disabled hidden>Select...</option>
                  {TUMOR_SIZES.map((item, i) =>
                    <option key={i} value={item.value}>{item.label}</option>
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
                  {TUMOR_GRADES.map((item, i) =>
                    <option key={i} value={item.value}>{item.label}</option>
                  )}
                </Select>
              )}
            </div>
            <div className={s.filter}>
              {getFieldDecorator('filters[num_pos_nodes]', {
                initialValue: '',
              })(
                <Select className={s.field} error={getFieldError('filters[num_pos_nodes]')}
                        label={'Number of Positive Nodes'}>
                  <option value='' disabled hidden>Select...</option>
                  {NUMBER_OF_NODES.map((item, i) =>
                    <option key={i} value={item.value}>{item.label}</option>
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
              {getFieldDecorator('filters[laterality]', {
                initialValue: '',
              })(
                <Select
                  onChange={(e) => this.changeField(e.target.value, 'laterality')}
                  className={s.field}
                  error={getFieldError('filters[laterality]')}
                  label={'Laterality'}
                >
                  <option value='' disabled hidden>Select...</option>
                  <option value='left'>Left</option>
                  <option value='right'>Right</option>
                </Select>
              )}
            </div>
            <div className={s.filter}>
              {getFieldDecorator('filters[site]', {
                initialValue: '',
              })(
                <Select
                  onChange={(e) => this.changeField(e.target.value, 'site')}
                  className={s.field}
                  error={getFieldError('filters[site]')}
                  label={'Site'}
                >
                  <option value='' disabled hidden>Select...</option>
                  {SITES.map((site, i) =>
                    <option key={i} value={site.value}>{site.label}</option>
                  )}
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
              {getFieldDecorator('filters[tumor_number]', {
                initialValue: '',
              })(
                <Select className={s.field} error={getFieldError('filters[tumor_number]')}
                        label={'Number of tumors'}>
                  <option value='' disabled hidden>Select...</option>
                  {NUMBER_OF_TUMORS.map((item, i) =>
                    <option key={i} value={item.value}>{item.label}</option>
                  )}
                </Select>
              )}
            </div>
            <div className={s.filter}>
              {getFieldDecorator('filters[stage]', {
                initialValue: '',
              })(
                <Select className={s.field} error={getFieldError('filters[stage]')} label={'Stage'}>
                  <option value='' disabled hidden>Select...</option>
                  {STAGES.map((item, i) =>
                    <option key={i} value={item.value}>{item.label}</option>
                  )}
                </Select>
              )}
            </div>
          </Col>
          <Col xs={24} md={16} className={s.chartColumn}>
            <Row type='flex' align='middle'>
              <Col xs={{span: 24, offset: 0}} md={{span: 8, offset: 8}} className={s.groupWrapper}>
                {getFieldDecorator('group', {
                  initialValue: '',
                  rules: [
                    {required: true, message: messages.required},
                  ]
                })(
                  <Select className={s.field} error={getFieldError('group')} label={'Group by'}>
                    <option value='' disabled hidden>Select...</option>

                    {GROUPED_SURVIVAL_MONTHS.map((group_by, i) =>
                      group_by.values ? (
                        <optgroup key={i} label={group_by.label}>
                          {group_by.values.map((item, j) =>
                            <option key={j}>{item}</option>
                          )}
                        </optgroup>
                      ) : (
                        <option key={i} value={group_by.value}>{group_by.label}</option>
                      )
                    )}
                  </Select>
                )}
              </Col>
              <Col xs={24} md={8} className={s.actions}>
                <a
                  className={s.clearFiltersBtn}
                  onClick={this.clearFilters}
                >
                  Clear filters
                </a>
                <div className={s.submitBtnWrapper}>
                  <Button bsStyle='primary' type='submit'>Submit</Button>
                </div>
              </Col>
            </Row>

            <div className={s.chartWrapper}>
              <Card
                loading={customAnalyticsLoading}
              >
                {((!isEmpty(customAnalytics.custom_analytics) && customAnalytics.custom_analytics.is_data === true) && customAnalytics.ca_type === 'survival_months') && (
                  <Row type='flex' gutter={16} className={s.content}>
                    <Col xs={24}>
                      {(!isEmpty(customAnalytics.custom_analytics) && customAnalytics.custom_analytics.top.is_data === true) && (
                        <div className={s.topChart}>
                          <Bar
                            data={{
                              ...customAnalytics.custom_analytics.top,
                              datasets: customAnalytics.custom_analytics.top.datasets.map(item => ({
                                ...item,
                                backgroundColor: color_1,
                                hoverBackgroundColor: color_3,
                                borderColor: white,
                              }))
                            }}
                            options={{
                              legend: {
                                display: false,
                                position: 'bottom',
                                labels: chartsLabelsOptions
                              },
                              scales: {
                                xAxes: [{
                                  barThickness: 75
                                }],
                                yAxes: [{
                                  ticks: {
                                    max: 100,
                                    beginAtZero: true,
                                    callback: (value) => `${value}%`
                                  }
                                }]
                              },
                              tooltips: {
                                callbacks: {
                                  label: formatChartNumber
                                }
                              },
                            }}
                            width={400}
                            height={100}
                            ref='chart'
                          />
                          <p className={s.chartTitle}>With Treatment</p>
                        </div>
                      )}
                      {(!isEmpty(customAnalytics.custom_analytics) && customAnalytics.custom_analytics.top.is_data === false) && (
                        <div className={s.emptyChart}>There is no available output for this set of filters</div>)}
                    </Col>
                    <Col xs={24}>
                      {(!isEmpty(customAnalytics.custom_analytics) && customAnalytics.custom_analytics.bottom.is_data === true) && (
                        <div className={s.bottomChart}>
                          <Bar
                            data={{
                              ...customAnalytics.custom_analytics.bottom,
                              datasets: customAnalytics.custom_analytics.bottom.datasets.map(item => ({
                                ...item,
                                backgroundColor: color_1,
                                hoverBackgroundColor: color_3,
                                borderColor: white,
                              }))
                            }}
                            options={{
                              legend: {
                                display: false,
                                position: 'bottom',
                                labels: chartsLabelsOptions
                              },
                              scales: {
                                xAxes: [{
                                  barThickness: 75
                                }],
                                yAxes: [{
                                  ticks: {
                                    max: 100,
                                    beginAtZero: true,
                                    callback: (value) => `${value}%`
                                  }
                                }]
                              },
                              tooltips: {
                                callbacks: {
                                  label: formatChartNumber
                                }
                              },
                            }}
                            width={400}
                            height={100}
                            ref='chart'
                          />
                          <p className={s.chartTitle}>Without Treatment</p>
                        </div>
                      )}
                      {(!isEmpty(customAnalytics.custom_analytics) && customAnalytics.custom_analytics.bottom.is_data === false) && (
                        <div className={s.emptyChart}>There is no available output for this set of filters</div>)}
                    </Col>
                  </Row>
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
  ...state.breastCancer,
})

const mapDispatch = {
  getCustomAnalytics,
}

export default connect(mapState, mapDispatch)(createForm()(withStyles(s)(BcSurvivalMonths)))