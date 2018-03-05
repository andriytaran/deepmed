import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './PcIndividualStatistics.css'
import {Bar, Pie} from 'react-chartjs-2'
import {formatChartNumber, getAgeRangeLabel} from '../../utils'
import {Card, Col, Row} from '../../components'
import isNil from 'lodash/isNil'
import isEmpty from 'lodash/isEmpty'

class PcIndividualStatistics extends React.Component {
  getPercent = (value) => {

    return value
  }
  render() {
    // TODO
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
    const {individualStatistics, diagnosisForm} = this.props
    const ageRange = diagnosisForm.age ? getAgeRangeLabel(diagnosisForm.age) : ''
    const ethnicity = diagnosisForm.ethnicity || ''

    return (
      <div className={s.container}>
        <div className={s.content}>
          <Row type='flex' gutter={16}>
            Individual Statistics
          </Row>
        </div>
      </div>
    )
  }
}

const mapState = state => ({
  ...state.prostateCancer,
})

const mapDispatch = {}

export default connect(mapState, mapDispatch)(withStyles(s)(PcIndividualStatistics))
