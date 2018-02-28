import React from 'react'
import {connect} from 'react-redux'
import s from './BcSurvivalMonths.css'
import {Col, Row, Spin} from '../../components'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import cn from 'classnames'
import isNil from 'lodash/isNil'
import Tab from 'react-bootstrap/lib/Tab'
import Tabs from 'react-bootstrap/lib/Tabs'
import isEmpty from 'lodash/isEmpty'
import {Bar} from 'react-chartjs-2'
import {formatChartNumber} from '../../utils'

const SurgeryTypesTable = ({items = [], visibleRowIndex}) =>
  <div className='table-responsive'>
    <table className={cn('table', s.surgeryTypesTable)}>
      <thead>
      <tr className={s.surgeryTypesTopHeader}>
        <th colSpan={3}><h6>SURGERY</h6></th>
      </tr>
      <tr className={s.surgeryTypesBottomHeader}>
        <th><h6>RECOMMENDATION</h6></th>
        <th><h6>TYPE</h6></th>
        <th className={s.borderRight}><h6>CONFIDENCE</h6></th>
      </tr>
      </thead>
      <tbody>
      {items[visibleRowIndex] ? (
        <tr>
          <td>{items[visibleRowIndex].surgery}</td>
          <td>{items[visibleRowIndex].type}</td>
          <td
            className={s.borderRight}>{items[visibleRowIndex].surgery_confidence_level}{items[visibleRowIndex].type === 'N/A' ? '' : '%'} </td>
        </tr>
      ) : (
        <tr>
          <td colSpan={7} style={{textAlign: 'center'}}>N/A</td>
        </tr>
      )}
      </tbody>
    </table>
  </div>

const chartsLabelsOptions = {
  boxWidth: 10,
  fontSize: 10,
  padding: 8
}

const white = '#fff'
const color_1 = 'rgba(72, 204, 245, 0.5)'
const color_2 = '#88d0d1'
const color_3 = '#47cfd1'
const color_4 = 'rgba(53, 109, 124, 0.5)'
const color_5 = '#1ac6ff'
const color_6 = '#8f61ec'
const color_7 = '#9df51d'
const color_8 = '#ff9400'
const color_9 = '#f51431'

const SurvivalMonthsChart = ({data}) =>
  <Bar
    data={{
      ...data.wo_treatment,
      datasets: [
        ...data.wo_treatment.datasets.map(item => ({
          ...item,
          backgroundColor: color_1,
          hoverBackgroundColor: color_1,
          borderColor: white,
          label: 'without treatment'
        })),
        ...data.treatment.datasets.map(item => ({
          ...item,
          backgroundColor: color_4,
          hoverBackgroundColor: color_4,
          borderColor: white,
          label: 'treatment',
        })),
      ]
    }}
    options={{
      legend: {
        position: 'bottom',
        labels: chartsLabelsOptions
      },
      scales: {
        xAxes: [{
          stacked: true,
          id: 'bar-x-axis1',
          barThickness: 50,
        }, {
          display: false,
          stacked: true,
          id: 'bar-x-axis2',
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
  />

class BcSurvivalMonths extends React.Component {
  state = {
    tab: 0,
  }

  changeTab = (tab) => {
    this.setState({tab})
  }

  render() {
    const {tab} = this.state
    const {diagnosis} = this.props

    return (
      <div className={s.container}>
        <div className={s.card}>
          <h2 className={s.cardHeader}>Recommended Treatment Plans</h2>
          <section className={s.section}>
            <div className={s.sectionContent}>
              <Tabs
                activeKey={tab}
                onSelect={this.changeTab}
                id='SurgeryTypesTabs'
                justified
                animation={false}
                className={s.surgeryTypesTabs}
              >
                <Tab eventKey={0} title='PREFERRED RECOMMENDATION'>
                  <SurgeryTypesTable items={diagnosis.overall_plans} visibleRowIndex={0}/>
                </Tab>
                <Tab eventKey={1} title='ALTERNATIVE RECOMMENDATION'>
                  <SurgeryTypesTable items={diagnosis.overall_plans} visibleRowIndex={1}/>
                </Tab>
              </Tabs>
            </div>
          </section>
          {(!isEmpty(diagnosis.overall_plans)) && (
            <div className={s.chartWrapper}>
              {!isEmpty(diagnosis.survival_months) && (
                <Row type='flex' gutter={16} className={s.content}>
                  <Col xs={24}>
                    <SurvivalMonthsChart
                      data={tab === 0 ? diagnosis.survival_months.preferred_plan : diagnosis.survival_months.alternative_plan}
                    />
                  </Col>
                </Row>
              )}
              {isNil(diagnosis.survival_months) && <Spin spinning/>}
            </div>
          )}
        </div>
      </div>
    )
  }
}

const mapState = state => ({
  ...state.breastCancer,
})

const mapDispatch = {}

export default connect(mapState, mapDispatch)(withStyles(s)(BcSurvivalMonths))
