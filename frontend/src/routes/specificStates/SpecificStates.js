import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './SpecificStates.scss'
import {Bar, HorizontalBar, Line, Pie} from 'react-chartjs-2'

class SpecificStates extends React.Component {
  render() {
    const color_1 = '#48ccf5'
    const color_2 = '#88d0d1'
    const color_3 = '#47cfd1'
    const color_4 = '#b8e8f5'
    const color_5 = '#1ac6ff'

    const chartsLabelsOptions = {
      boxWidth: 10,
      fontSize: 10,
      padding: 8
    }
    const {data} = this.props
    return (
      <div className="container container-full" data-children="same-height">
        <div className="row">
          <div className="col-sm-12">
            <div className="custom-panel custom-panel-condensed light-gray-bg">
              <div className="row row-condensed">
                {data.woman_age_30_40_annualy_diagnosed && (
                  <div className="col-xl-5ths col-lg-4 col-md-6">
                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                         data-adjust="height">
                      <h4 className="push-top-1 push-bot-2 text-center" data-type="title">
                        <strong># of Women Age 30-40 Annually Diagnosed</strong>
                      </h4>
                      <Line
                        data={data.woman_age_30_40_annualy_diagnosed}
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
                        height={400}
                      />
                    </div>
                  </div>
                )}
                {data.growth_by_specific_type && (
                  <div className="col-xl-5ths col-lg-4 col-md-6">
                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                         data-adjust="height">
                      <h4 className="push-top-1 push-bot-2 text-center" data-type="title">
                        <strong>ER+ / PR- / HER2- Annual Diagnoses</strong>
                      </h4>
                      <Line
                        data={{
                          ...data.growth_by_specific_type.other,
                          datasets: [
                            ...data.growth_by_specific_type.other.datasets,
                            ...data.growth_by_specific_type.idc.datasets,
                            ...data.growth_by_specific_type.ilc.datasets,
                            ...data.growth_by_specific_type.in_situ.datasets,
                          ]
                        }}
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
                        height={400}
                      />
                    </div>
                  </div>
                )}
                {data.breast_cancer_by_grade_and_size_age_30_40 && (
                  <div className="col-xl-5ths col-lg-4 col-md-6">
                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0" data-adjust="height">
                      <h4 className="push-top-1 push-bot-2 text-center" data-type="title">
                        <strong>Breast Cancer by Grade and Size (Age 30-40)</strong>
                      </h4>
                      <Bar
                        data={{
                          ...data.breast_cancer_by_grade_and_size_age_30_40.grade,
                          datasets: data.breast_cancer_by_grade_and_size_age_30_40.grade.datasets.map(item => ({
                            ...item,
                            backgroundColor: color_1,
                            hoverBackgroundColor: color_3,
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
                          ...data.breast_cancer_by_grade_and_size_age_30_40.size,
                          datasets: data.breast_cancer_by_grade_and_size_age_30_40.size.datasets.map(item => ({
                            ...item,
                            backgroundColor: color_1,
                            hoverBackgroundColor: color_3,
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
                {data.distribution_of_stage_of_cancer_for_ages_30_40 && (
                  <div className="col-xl-5ths col-lg-4 col-md-6">
                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                         data-adjust="height">
                      <h4 className="push-top-1 push-bot-2 text-center" data-type="title">
                        <strong>Distribution of Stage of Cancer for Women Ages 30-40</strong>
                      </h4>
                      <Pie
                        data={{
                          ...data.distribution_of_stage_of_cancer_for_ages_30_40,
                          datasets: data.distribution_of_stage_of_cancer_for_ages_30_40.datasets.map(item => ({
                            ...item,
                            backgroundColor: [color_1, color_3, color_4, color_2, color_5],
                          }))
                        }}
                        options={{
                          legend: {
                            display: true,
                            position: 'bottom',
                            labels: chartsLabelsOptions
                          }
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
                        <strong>% of Women with Cancer by Race</strong>
                      </h4>
                      <p className="no-margin pad-left-1 small"><strong>Overall</strong></p>
                      <Pie
                        data={{
                          ...data.percent_of_women_with_cancer_by_race.overall,
                          datasets: data.percent_of_women_with_cancer_by_race.overall.datasets.map(item => ({
                            ...item,
                            backgroundColor: [color_1, color_3, color_4, color_2],
                          }))
                        }}
                        options={{
                          legend: {
                            display: true,
                            position: 'right',
                            labels: chartsLabelsOptions
                          }
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
                            backgroundColor: [color_1, color_3, color_4, color_2],
                          }))
                        }}
                        options={{
                          legend: {
                            display: true,
                            position: 'right',
                            labels: chartsLabelsOptions
                          }
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
                {data.surgery_decisions_within_ages_30_40 && (
                  <div className="col-xl-5ths col-lg-4 col-md-6">
                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0" data-adjust="height">
                      <h4 className="push-top-1 push-bot-2 text-center" data-type="title">
                        <strong>Surgery Decisions for Women Within Ages 30-40</strong>
                      </h4>
                      <Pie
                        data={{
                          ...data.surgery_decisions_within_ages_30_40,
                          datasets: data.surgery_decisions_within_ages_30_40.datasets.map(item => ({
                            ...item,
                            backgroundColor: [color_1, color_3, color_4, color_2, color_5],
                          }))
                        }}
                        options={{
                          legend: {
                            display: true,
                            position: 'bottom',
                            labels: chartsLabelsOptions
                          }
                        }}
                        width={400}
                        height={400}
                      />
                    </div>
                  </div>
                )}
                {data.chemotherapy_for_ages_30_40 && (
                  <div className="col-xl-5ths col-lg-4 col-md-6">
                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                         data-adjust="height">
                      <h4 className="push-top-1 push-bot-2 text-center" data-type="title">
                        <strong>Chemotherapy for Women Ages 30-40</strong>
                      </h4>
                      <p className="no-margin pad-left-1 small"><strong>Overall</strong></p>
                      <Pie
                        data={{
                          ...data.chemotherapy_for_ages_30_40,
                          datasets: data.chemotherapy_for_ages_30_40.datasets.map(item => ({
                            ...item,
                            backgroundColor: [color_1, color_3],
                          }))
                        }}
                        options={{
                          legend: {
                            display: true,
                            position: 'right',
                            labels: chartsLabelsOptions
                          }
                        }}
                        width={200}
                        height={75}
                      />
                      <p className="push-bot-0 push-top-3 pad-left-1 small"><strong>Breakout<br/>by Stage</strong>
                      </p>
                      <Pie data={{
                        labels: ['Stage 0. 10%', 'Stage 1. 25%', 'Stage 2. 10%', 'Stage 3. 30%'],
                        datasets: [{
                          backgroundColor: [color_1, color_3, color_4, color_2, color_5],
                          data: [10, 25, 30, 10, 30]
                        }]
                      }} options={{
                        legend: {
                          display: true,
                          position: 'right',
                          labels: chartsLabelsOptions
                        }
                      }} width={200} height={75}/>
                    </div>
                  </div>
                )}
                {data.radiation_for_ages_30_40 && (
                  <div className="col-xl-5ths col-lg-4 col-md-6">
                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                         data-adjust="height">
                      <h4 className="push-top-1 push-bot-2 text-center" data-type="title">
                        <strong>Radiation for Women Ages 30-40</strong>
                      </h4>
                      <p className="no-margin pad-left-1 small"><strong>Overall</strong></p>
                      <Pie
                        data={{
                          ...data.radiation_for_ages_30_40,
                          datasets: data.radiation_for_ages_30_40.datasets.map(item => ({
                            ...item,
                            backgroundColor: [color_1, color_3],
                          }))
                        }}
                        options={{
                          legend: {
                            display: true,
                            position: 'right',
                            labels: chartsLabelsOptions
                          }
                        }}
                        width={200}
                        height={75}
                      />
                      <p className="push-bot-0 push-top-3 pad-left-1 small"><strong>Breakout<br/>by Stage</strong>
                      </p>
                      <Pie data={{
                        labels: ['Stage 0. 30%', 'Stage 1. 25%', 'Stage 2. 30%', 'Stage 3. 10%'],
                        datasets: [{
                          backgroundColor: [color_1, color_3, color_4, color_2, color_5],
                          data: [30, 25, 30, 10, 5]
                        }]
                      }} options={{
                        legend: {
                          display: true,
                          position: 'right',
                          labels: chartsLabelsOptions
                        }
                      }} width={200} height={75}/>
                    </div>
                  </div>
                )}
                {data.survival_months_within_ages_30_40 && (
                  <div className="col-xl-5ths col-lg-4 col-md-6">
                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                         data-adjust="height">
                      <h4 className="push-top-1 push-bot-2 text-center" data-type="title">
                        <strong>Survival Months for Women Ages 30-40</strong>
                      </h4>
                      <HorizontalBar
                        data={{
                          ...data.survival_months_within_ages_30_40,
                          datasets: data.survival_months_within_ages_30_40.datasets.map(item => ({
                            ...item,
                            backgroundColor: color_1,
                            hoverBackgroundColor: color_3,
                          }))
                        }}
                        options={{
                          legend: {
                            display: false,
                            position: 'bottom'
                          },
                          scales: {
                            xAxes: [{
                              ticks: {
                                beginAtZero: true
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
                {data.cause_of_death && (
                  <div className="col-xl-5ths col-lg-4 col-md-6">
                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                         data-adjust="height">
                      <h4 className="push-top-1 push-bot-2 text-center" data-type="title">
                        <strong>Cause of Death</strong></h4>
                      <p className="no-margin pad-left-1 small"><strong>Overall</strong></p>
                      <Pie
                        data={{
                          ...data.cause_of_death.cause_of_death_overall,
                          datasets: data.cause_of_death.cause_of_death_overall.datasets.map(item => ({
                            ...item,
                            backgroundColor: [color_1, color_3],
                          }))
                        }}
                        options={{
                          legend: {
                            display: true,
                            position: 'right',
                            labels: chartsLabelsOptions
                          }
                        }}
                        width={200}
                        height={75}
                      />
                      <p className="push-bot-0 push-top-3 pad-left-1 small">
                        <strong>Ages<br/>30-40</strong>
                      </p>
                      <Pie
                        data={{
                          ...data.cause_of_death.cause_of_death_within_ages_30_40,
                          datasets: data.cause_of_death.cause_of_death_within_ages_30_40.datasets.map(item => ({
                            ...item,
                            backgroundColor: [color_1, color_3],
                          }))
                        }}
                        options={{
                          legend: {
                            display: true,
                            position: 'right',
                            labels: chartsLabelsOptions
                          }
                        }}
                        width={200}
                        height={75}
                      />
                    </div>
                  </div>
                )}
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
