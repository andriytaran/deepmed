import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './SpecificStates.scss'
import {Bar, Pie} from 'react-chartjs-2'
import {formatChartNumber, getAgeRangeLabel} from '../../utils'
import {Col, Row} from '../../components'

class SpecificStates extends React.Component {
  render() {
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
      <div className='container container-full'>
        <div className='custom-panel custom-panel-condensed light-gray-bg'>
          <Row type='flex' gutter={16}>
            {individualStatistics.percent_women_annualy_diagnosed && (
              <Col xs={24} sm={12} md={8} className={s.col}>
                <div className={s.card}>
                  <h4 className={s.header}>
                    <strong>Women Ages {ageRange} as a Percent of total Diagnoses</strong>
                  </h4>
                  <Bar
                    data={{
                      ...individualStatistics.percent_women_annualy_diagnosed,
                      datasets: individualStatistics.percent_women_annualy_diagnosed.datasets.map(item => ({
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
                        yAxes: [{
                          ticks: {
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
                    height={400}
                    ref='chart'
                  />
                </div>
              </Col>
            )}
            {individualStatistics.percent_women_by_type && (
              <Col xs={24} sm={12} md={8} className={s.col}>
                <div className={s.card}>
                  <h4 className={s.header}>
                    <strong>Percent of Women by Breast Cancer Type</strong>
                  </h4>
                  <Pie
                    data={{
                      ...individualStatistics.percent_women_by_type,
                      datasets: individualStatistics.percent_women_by_type.datasets.map(item => ({
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
                    height={400}
                  />
                </div>
              </Col>
            )}
            {individualStatistics.percent_of_women_with_cancer_by_race && (
              <Col xs={24} sm={12} md={8} className={s.col}>
                <div className={s.card}>
                  <h4 className={s.header}>
                    <strong>% of Women with Cancer by Ethnicity {ageRange}</strong>
                  </h4>
                  <p className='no-margin pad-left-1 small'><strong>Overall</strong></p>
                  <Pie
                    data={{
                      ...individualStatistics.percent_of_women_with_cancer_by_race.overall,
                      datasets: individualStatistics.percent_of_women_with_cancer_by_race.overall.datasets.map(item => ({
                        ...item,
                        backgroundColor: [color_1, color_3, color_4, color_2, color_5, color_6, color_7, color_8, color_9],
                        borderColor: white,
                      }))
                    }}
                    options={{
                      legend: {
                        display: true,
                        position: 'right',
                        labels: chartsLabelsOptions
                      },
                      tooltips: {
                        callbacks: {
                          label: formatChartNumber
                        }
                      },
                    }}
                    width={400}
                    height={150}
                  />
                  <p className='push-bot-0 push-top-3 pad-left-1 small'><strong>Within Your<br/>Age Bracket</strong>
                  </p>
                  <Pie
                    data={{
                      ...individualStatistics.percent_of_women_with_cancer_by_race.by_age,
                      datasets: individualStatistics.percent_of_women_with_cancer_by_race.by_age.datasets.map(item => ({
                        ...item,
                        backgroundColor: [color_1, color_3, color_4, color_2, color_5, color_6, color_7, color_8, color_9],
                        borderColor: white,
                      }))
                    }}
                    options={{
                      legend: {
                        display: true,
                        position: 'right',
                        labels: chartsLabelsOptions
                      },
                      tooltips: {
                        callbacks: {
                          label: formatChartNumber
                        }
                      },
                    }}
                    width={400}
                    height={150}
                  />
                </div>
              </Col>
            )}
            {individualStatistics.breast_cancer_by_grade_and_size && (
              <Col xs={24} sm={12} md={8} className={s.col}>
                <div className={s.card}>
                  <h4 className={s.header}>
                    <strong>Breast Cancer by Grade {ageRange}</strong>
                  </h4>
                  <Bar
                    data={{
                      ...individualStatistics.breast_cancer_by_grade_and_size.grade,
                      datasets: individualStatistics.breast_cancer_by_grade_and_size.grade.datasets.map(item => ({
                        ...item,
                        backgroundColor: color_1,
                        borderColor: white,
                      }))
                    }}
                    options={{
                      legend: {
                        display: false,
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
                    height={400}
                  />
                </div>
              </Col>
            )}
            {individualStatistics.breast_cancer_by_grade_and_size && (
              <Col xs={24} sm={12} md={8} className={s.col}>
                <div className={s.card}>
                  <h4 className={s.header}>
                    <strong>Breast Cancer by Tumor Size {ageRange}</strong>
                  </h4>
                  <Bar
                    data={{
                      ...individualStatistics.breast_cancer_by_grade_and_size.size,
                      datasets: individualStatistics.breast_cancer_by_grade_and_size.size.datasets.map(item => ({
                        ...item,
                        backgroundColor: color_1,
                        borderColor: white,
                      }))
                    }}
                    options={{
                      legend: {
                        display: false,
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
                    height={400}
                  />
                </div>
              </Col>
            )}
            {individualStatistics.distribution_of_stage_of_cancer && (
              <Col xs={24} sm={12} md={8} className={s.col}>
                <div className={s.card}>
                  <h4 className={s.header}>
                    <strong>% of Women with Cancer by Stage {ageRange}</strong>
                  </h4>
                  <p className='no-margin pad-left-1 small'><strong>Overall</strong></p>
                  <Pie
                    data={{
                      ...individualStatistics.distribution_of_stage_of_cancer.overall,
                      datasets: individualStatistics.distribution_of_stage_of_cancer.overall.datasets.map(item => ({
                        ...item,
                        backgroundColor: [color_1, color_3, color_4, color_2, color_5, color_6, color_7, color_8, color_9],
                        borderColor: white,
                      }))
                    }}
                    options={{
                      legend: {
                        display: true,
                        position: 'right',
                        labels: chartsLabelsOptions
                      },
                      tooltips: {
                        callbacks: {
                          label: formatChartNumber
                        }
                      },
                    }}
                    width={400}
                    height={150}
                  />
                  <p className='push-bot-0 push-top-3 pad-left-1 small'><strong>{ethnicity} Women Only</strong>
                  </p>
                  <Pie
                    data={{
                      ...individualStatistics.distribution_of_stage_of_cancer.by_race,
                      datasets: individualStatistics.distribution_of_stage_of_cancer.by_race.datasets.map(item => ({
                        ...item,
                        backgroundColor: [color_1, color_3, color_4, color_2, color_5, color_6, color_7, color_8, color_9],
                        borderColor: white,
                      }))
                    }}
                    options={{
                      legend: {
                        display: true,
                        position: 'right',
                        labels: chartsLabelsOptions
                      },
                      tooltips: {
                        callbacks: {
                          label: formatChartNumber
                        }
                      },
                    }}
                    width={400}
                    height={150}
                  />
                </div>
              </Col>
            )}
            {individualStatistics.surgery_decisions && (
              <Col xs={24} sm={12} md={8} className={s.col}>
                <div className={s.card}>
                  <h4 className={s.header}>
                    <strong>Surgery Decisions for Women {ageRange}</strong>
                  </h4>
                  <Pie
                    data={{
                      ...individualStatistics.surgery_decisions,
                      datasets: individualStatistics.surgery_decisions.datasets.map(item => ({
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
                    height={400}
                  />
                </div>
              </Col>
            )}
            {individualStatistics.chemotherapy && (
              <Col xs={24} sm={12} md={8} className={s.col}>
                <div className={s.card}>
                  <h4 className={s.header}>
                    <strong>Chemotherapy for Women {ageRange}</strong>
                  </h4>
                  <p className='no-margin pad-left-1 small'><strong>Overall</strong></p>
                  <Pie
                    data={{
                      ...individualStatistics.chemotherapy.overall,
                      datasets: individualStatistics.chemotherapy.overall.datasets.map(item => ({
                        ...item,
                        backgroundColor: [color_1, color_3, color_4, color_2, color_5, color_6, color_7, color_8, color_9],
                        borderColor: white,
                      }))
                    }}
                    options={{
                      legend: {
                        display: true,
                        position: 'right',
                        labels: chartsLabelsOptions
                      },
                      tooltips: {
                        callbacks: {
                          label: formatChartNumber
                        }
                      },
                    }}
                    width={400}
                    height={150}
                  />
                  <p className='push-bot-0 push-top-3 pad-left-1 small'><strong>by Stage</strong>
                  </p>
                  <Pie
                    data={{
                      ...individualStatistics.chemotherapy.breakout_by_stage,
                      datasets: individualStatistics.chemotherapy.breakout_by_stage.datasets.map(item => ({
                        ...item,
                        backgroundColor: [color_1, color_3, color_4, color_2, color_5, color_6, color_7, color_8, color_9],
                        borderColor: white,
                      }))
                    }}
                    options={{
                      legend: {
                        display: true,
                        position: 'right',
                        labels: chartsLabelsOptions
                      },
                      tooltips: {
                        callbacks: {
                          label: formatChartNumber
                        }
                      },
                    }}
                    width={400}
                    height={150}
                  />
                </div>
              </Col>
            )}
            {individualStatistics.radiation && (
              <Col xs={24} sm={12} md={8} className={s.col}>
                <div className={s.card}>
                  <h4 className={s.header}>
                    <strong>Radiation for Women {ageRange}</strong>
                  </h4>
                  <p className='no-margin pad-left-1 small'><strong>Overall</strong></p>
                  <Pie
                    data={{
                      ...individualStatistics.radiation.overall,
                      datasets: individualStatistics.radiation.overall.datasets.map(item => ({
                        ...item,
                        backgroundColor: [color_1, color_3, color_4, color_2, color_5, color_6, color_7, color_8, color_9],
                        borderColor: white,
                      }))
                    }}
                    options={{
                      legend: {
                        display: true,
                        position: 'right',
                        labels: chartsLabelsOptions,
                      },
                      tooltips: {
                        callbacks: {
                          label: formatChartNumber
                        }
                      },
                    }}
                    width={400}
                    height={160}
                  />
                  <p className='push-bot-0 push-top-3 pad-left-1 small'><strong>by Stage</strong>
                  </p>
                  <Pie
                    data={{
                      ...individualStatistics.radiation.breakout_by_stage,
                      datasets: individualStatistics.radiation.breakout_by_stage.datasets.map(item => ({
                        ...item,
                        backgroundColor: [color_1, color_3, color_4, color_2, color_5, color_6, color_7, color_8, color_9],
                        borderColor: white,
                      }))
                    }}
                    options={{
                      legend: {
                        display: true,
                        position: 'right',
                        labels: chartsLabelsOptions,
                      },
                      tooltips: {
                        callbacks: {
                          label: formatChartNumber
                        }
                      },
                    }}
                    width={400}
                    height={160}
                  />
                </div>
              </Col>
            )}
          </Row>
        </div>
      </div>
    )
  }
}

const mapState = state => ({
  ...state.diagnosis,
})

const mapDispatch = {}

export default connect(mapState, mapDispatch)(withStyles(s)(SpecificStates))
