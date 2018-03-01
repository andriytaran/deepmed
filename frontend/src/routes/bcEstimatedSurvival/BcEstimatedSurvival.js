import React from 'react'
import {connect} from 'react-redux'
import s from './BcEstimatedSurvival.css'
import {Col, Row, Spin} from '../../components'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import cn from 'classnames'
import isNil from 'lodash/isNil'
import Tab from 'react-bootstrap/lib/Tab'
import Tabs from 'react-bootstrap/lib/Tabs'
import isEmpty from 'lodash/isEmpty'
import {Bar} from 'react-chartjs-2'
import {formatLabel} from '../../utils'

const SurgeryTypesTable = ({items = [], visibleRowIndex}) =>
  <div className='table-responsive'>
  </div>

const chartsLabelsOptions = {
  boxWidth: 10,
  fontSize: 10,
  padding: 8
}

const white = '#fff'
const color_1 = 'rgba(72, 204, 245, 0.75)'
const color_2 = '#88d0d1'
const color_3 = '#47cfd1'
const color_4 = 'rgba(184, 232, 245, 0.5)'
const color_5 = 'rgba(0, 125, 255, 0.75)'
const color_6 = 'rgba(143, 97, 236, 0.75)'
const color_7 = '#9df51d'
const color_8 = '#ff9400'
const color_9 = '#f51431'

const BcEstimatedSurvivalChart = ({data}) =>
  <Bar
    data={{
      labels: data.wo_decision.labels,
      datasets: [
        ...data.wo_decision.datasets.map(item => ({
          ...item,
          backgroundColor: color_1,
          hoverBackgroundColor: color_1,
          borderColor: white,
          label: data.wo_decision.chart_label,
        })),
        ...data.decision.datasets.map(item => ({
          ...item,
          backgroundColor: color_5 ,
          hoverBackgroundColor: color_5,
          borderColor: white,
          label: data.decision.chart_label,
        })),
      ]
    }}
    redraw
    options={{
      legend: {
        position: 'bottom',
        labels: chartsLabelsOptions
      },
      scales: {
        xAxes: [{
          id: 'bar-x-axis1',
          barPercentage: 1.0,
          categoryPercentage: 0.3
        }],
        yAxes: [{
          ticks: {
            max: 100,
            beginAtZero: true,
            callback: (value) => `${value}%`
          },
        }],
      },
      tooltips: {
        callbacks: {
          label: formatLabel,
        }
      },
    }}
  />

class BcBcEstimatedSurvival extends React.Component {
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
                id='surgeryTypesTabs'
                justified
                animation={false}
                className={s.surgeryTypesTabs}
              >
                <Tab eventKey={0} title='Chemotherapy Decision'>
                  <SurgeryTypesTable items={diagnosis.overall_plans} visibleRowIndex={0}/>
                </Tab>
                <Tab eventKey={1} title='Surgery Decision'>
                  <SurgeryTypesTable items={diagnosis.overall_plans} visibleRowIndex={1}/>
                </Tab>
              </Tabs>
            </div>
          </section>
          {(!isEmpty(diagnosis.overall_plans)) && (
            <div className={s.chartWrapper}>
              <h3 className={s.chartHeader}>Estimated Survival Rate for your Diagnosis</h3>
              {!isEmpty(diagnosis.estimated_survival) && (
                <Row type='flex' gutter={16} className={s.content}>
                  <Col xs={24}>
                    {tab === 0 ? (
                      <BcEstimatedSurvivalChart data={diagnosis.estimated_survival.chemo_decision}/>
                    ) : (
                      <BcEstimatedSurvivalChart data={diagnosis.estimated_survival.surgery_decision}/>
                    )}
                  </Col>
                </Row>
              )}
              {isNil(diagnosis.estimated_survival) && <Spin spinning/>}
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

export default connect(mapState, mapDispatch)(withStyles(s)(BcBcEstimatedSurvival))
