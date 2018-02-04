import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './SpecificStates.scss'
import {Bar, Line, Pie} from 'react-chartjs-2'
import {formatChartNumber} from '../../utils'

// TODO
const getAgeRangeLabel = (age) => {
  const nearestRoundedDown10 = parseInt(+age / 10, 10) * 10
  return `Ages ${nearestRoundedDown10}-${nearestRoundedDown10 + 10}`
}

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
    const color_8 = '#ff9200'
    const color_9 = '#f51431'

    const chartsLabelsOptions = {
      boxWidth: 10,
      fontSize: 10,
      padding: 8
    }
    const {data, diagnosisForm} = this.props
    const ageRange = diagnosisForm.age ? getAgeRangeLabel(diagnosisForm.age) : ''
    return (
      <div className="container container-full" data-children="same-height">
        <div className="row">
          <div className="col-sm-12">
            <div className="custom-panel custom-panel-condensed light-gray-bg">
              <div className="row row-condensed">
            {data.woman_annualy_diagnosed && (
              <div className="col-xl-12 col-lg-12 col-md-12">
                <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                     data-adjust="height">
                  <h4 className="push-top-1 push-bot-2 text-center" data-type="title">
                    <strong># of Women Annually Diagnosed {ageRange}</strong>
                  </h4>
                  <Line
                    data={data.woman_annualy_diagnosed}
                    options={{
                      legend: {
                        display: false,
                        position: 'bottom'
                      },
                      scales: {
                        yAxes: [{
                          gridLines: {
                            display: false
                          },
                          ticks: {
                            beginAtZero: true,
                          }
                        }]
                      }
                    }}
                    width={400}
                    height={100}
                  />
                </div>
              </div>
            )}
              </div>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-sm-12">
            <div className="custom-panel custom-panel-condensed light-gray-bg">
              <div className="row row-condensed">
                {data.growth_by_specific_type && (
                  <div className="col-xl-5ths col-lg-4 col-md-6">
                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                         data-adjust="height">
                      <h4 className="push-top-1 push-bot-2 text-center" data-type="title">
                        <strong>Breast Cancer Trends by Specific Type</strong>
                      </h4>
                      <Line
                        data={data.growth_by_specific_type}
                        options={{
                          legend: {
                            position: 'bottom',
                            display: false
                          },
                          scales: {
                            yAxes: [{
                              gridLines: {
                                display: false
                              },
                              ticks: {
                                beginAtZero: true,
                              }
                            }]
                          }
                        }}
                        width={400}
                        height={400}
                      />
                    </div>
                  </div>
                )}
                {data.breast_cancer_by_grade_and_size && (
                  <div className="col-xl-5ths col-lg-4 col-md-6">
                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0" data-adjust="height">
                      <h4 className="push-top-1 push-bot-2 text-center" data-type="title">
                        <strong>Breast Cancer by Grade and Size {ageRange}</strong>
                      </h4>
                      <Bar
                        data={{
                          ...data.breast_cancer_by_grade_and_size.grade,
                          datasets: data.breast_cancer_by_grade_and_size.grade.datasets.map(item => ({
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
                          }
                        }}
                        width={200}
                        height={100}
                        ref="chart"
                      />
                      <Bar
                        data={{
                          ...data.breast_cancer_by_grade_and_size.size,
                          datasets: data.breast_cancer_by_grade_and_size.size.datasets.map(item => ({
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
                          }
                        }}
                        width={200}
                        height={100}
                      />
                    </div>
                  </div>
                )}
                {data.distribution_of_stage_of_cancer && (
                  <div className="col-xl-5ths col-lg-4 col-md-6">
                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                         data-adjust="height">
                      <h4 className="push-top-1 push-bot-2 text-center" data-type="title">
                        <strong>Distribution of Stage of Cancer for Women {ageRange}</strong>
                      </h4>
                      <Pie
                        data={{
                          ...data.distribution_of_stage_of_cancer,
                          datasets: data.distribution_of_stage_of_cancer.datasets.map(item => ({
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
                  </div>
                )}
                {data.percent_of_women_with_cancer_by_race && (
                  <div className="col-xl-5ths col-lg-4 col-md-6">
                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0" data-adjust="height">
                      <h4 className="push-top-1 push-bot-2 text-center" data-type="title">
                        <strong>% of Women with Cancer by Race {ageRange}</strong>
                      </h4>
                      <p className="no-margin pad-left-1 small"><strong>Overall</strong></p>
                      <Pie
                        data={{
                          ...data.percent_of_women_with_cancer_by_race.overall,
                          datasets: data.percent_of_women_with_cancer_by_race.overall.datasets.map(item => ({
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
                        width={200}
                        height={75}
                      />
                      <p className="push-bot-0 push-top-3 pad-left-1 small"><strong>Within Your<br/>Age Bracket</strong>
                      </p>
                      <Pie
                        data={{
                          ...data.percent_of_women_with_cancer_by_race.by_age,
                          datasets: data.percent_of_women_with_cancer_by_race.by_age.datasets.map(item => ({
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
                        width={200}
                        height={75}
                      />
                    </div>
                  </div>
                )}
              </div>
            </div>
            <div className="custom-panel custom-panel-condensed light-gray-bg push-bot-0">
              <div className="row row-condensed">
                {data.surgery_decisions && (
                  <div className="col-xl-5ths col-lg-4 col-md-6">
                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0" data-adjust="height">
                      <h4 className="push-top-1 push-bot-2 text-center" data-type="title">
                        <strong>Surgery Decisions for Women Within {ageRange}</strong>
                      </h4>
                      <Pie
                        data={{
                          ...data.surgery_decisions,
                          datasets: data.surgery_decisions.datasets.map(item => ({
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
                  </div>
                )}
                {data.chemotherapy && (
                  <div className="col-xl-5ths col-lg-4 col-md-6">
                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                         data-adjust="height">
                      <h4 className="push-top-1 push-bot-2 text-center" data-type="title">
                        <strong>Chemotherapy for Women {ageRange}</strong>
                      </h4>
                      <p className="no-margin pad-left-1 small"><strong>Overall</strong></p>
                      <Pie
                        data={{
                          ...data.chemotherapy.overall,
                          datasets: data.chemotherapy.overall.datasets.map(item => ({
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
                        width={200}
                        height={75}
                      />
                      <p className="push-bot-0 push-top-3 pad-left-1 small"><strong>Breakout<br/>by Stage</strong>
                      </p>
                      <Pie
                        data={{
                          ...data.chemotherapy.breakout_by_stage,
                          datasets: data.chemotherapy.breakout_by_stage.datasets.map(item => ({
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
                        width={200}
                        height={75}
                      />
                    </div>
                  </div>
                )}
                {data.radiation && (
                  <div className="col-xl-5ths col-lg-4 col-md-6">
                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                         data-adjust="height">
                      <h4 className="push-top-1 push-bot-2 text-center" data-type="title">
                        <strong>Radiation for Women {ageRange}</strong>
                      </h4>
                      <p className="no-margin pad-left-1 small"><strong>Overall</strong></p>
                      <Pie
                        data={{
                          ...data.radiation.overall,
                          datasets: data.radiation.overall.datasets.map(item => ({
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
                        width={200}
                        height={75}
                      />
                      <p className="push-bot-0 push-top-3 pad-left-1 small"><strong>Breakout<br/>by Stage</strong>
                      </p>
                      <Pie
                        data={{
                          ...data.radiation.breakout_by_stage,
                          datasets: data.radiation.breakout_by_stage.datasets.map(item => ({
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
                        width={200}
                        height={75}
                      />
                    </div>
                  </div>
                )}
                {/*{data.survival_months && (*/}
                {/*<div className="col-xl-5ths col-lg-4 col-md-6">*/}
                {/*<div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"*/}
                {/*data-adjust="height">*/}
                {/*<h4 className="push-top-1 push-bot-2 text-center" data-type="title">*/}
                {/*<strong>Survival Months for Women {ageRange}</strong>*/}
                {/*</h4>*/}
                {/*<HorizontalBar*/}
                {/*data={{*/}
                {/*...data.survival_months,*/}
                {/*datasets: data.survival_months.datasets.map(item => ({*/}
                {/*...item,*/}
                {/*backgroundColor: color_1,*/}
                {/*hoverBackgroundColor: color_3,*/}
                {/*}))*/}
                {/*}}*/}
                {/*options={{*/}
                {/*legend: {*/}
                {/*display: false,*/}
                {/*position: 'bottom'*/}
                {/*},*/}
                {/*scales: {*/}
                {/*xAxes: [{*/}
                {/*ticks: {*/}
                {/*beginAtZero: true*/}
                {/*}*/}
                {/*}]*/}
                {/*}*/}
                {/*}}*/}
                {/*width={400}*/}
                {/*height={400}*/}
                {/*/>*/}
                {/*</div>*/}
                {/*</div>*/}
                {/*)}*/}
                {/*{data.cause_of_death && (*/}
                {/*<div className="col-xl-5ths col-lg-4 col-md-6">*/}
                {/*<div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"*/}
                {/*data-adjust="height">*/}
                {/*<h4 className="push-top-1 push-bot-2 text-center" data-type="title">*/}
                {/*<strong>Cause of Death</strong></h4>*/}
                {/*<p className="no-margin pad-left-1 small"><strong>Overall</strong></p>*/}
                {/*<Pie*/}
                {/*data={{*/}
                {/*...data.cause_of_death.cause_of_death_overall,*/}
                {/*datasets: data.cause_of_death.cause_of_death_overall.datasets.map(item => ({*/}
                {/*...item,*/}
                {/*backgroundColor: [color_1, color_3, color_4, color_2, color_5, color_6, color_7, color_8, color_9],*/}
                {/*}))*/}
                {/*}}*/}
                {/*options={{*/}
                {/*legend: {*/}
                {/*display: true,*/}
                {/*position: 'right',*/}
                {/*labels: chartsLabelsOptions*/}
                {/*}*/}
                {/*}}*/}
                {/*width={200}*/}
                {/*height={75}*/}
                {/*/>*/}
                {/*<p className="push-bot-0 push-top-3 pad-left-1 small">*/}
                {/*<strong>{ageRange}</strong>*/}
                {/*</p>*/}
                {/*<Pie*/}
                {/*data={{*/}
                {/*...data.cause_of_death.by_ages,*/}
                {/*datasets: data.cause_of_death.by_ages.datasets.map(item => ({*/}
                {/*...item,*/}
                {/*backgroundColor: [color_1, color_3, color_4, color_2, color_5, color_6, color_7, color_8, color_9],*/}
                {/*}))*/}
                {/*}}*/}
                {/*options={{*/}
                {/*legend: {*/}
                {/*display: true,*/}
                {/*position: 'right',*/}
                {/*labels: chartsLabelsOptions*/}
                {/*}*/}
                {/*}}*/}
                {/*width={200}*/}
                {/*height={75}*/}
                {/*/>*/}
                {/*</div>*/}
                {/*</div>*/}
                {/*)}*/}
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

const mapDispatch = {}

export default connect(mapState, mapDispatch)(withStyles(s)(SpecificStates))
