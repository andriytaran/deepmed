import React from 'react';
import {push} from 'react-router-redux';
import {connect} from 'react-redux';
import {Field, reduxForm} from 'redux-form';
import {bindActionCreators} from 'redux';
import PropTypes from 'prop-types';

import { Line, Bar } from 'react-chartjs-2';

import './style.scss';

class SpecificStatesView extends React.Component {
    static propTypes = {
        token: PropTypes.string.isRequired,
        dispatch: PropTypes.func.isRequired,
    };

    state = {
        showDetails: false
    };

    render() {
        // Colors
        const color_1 = '#48ccf5';
        const color_2 = '#88d0d1';
        const color_3 = '#47cfd1';
        const color_4 = '#b8e8f5';
        const color_5 = '#1ac6ff';

        // const ctx = this.refs.chart.getContext('2d');
        // const gradient = ctx.createLinearGradient(0, 0, 0, 100);
		// gradient.addColorStop(1, color_3);
		// gradient.addColorStop(0, color_1);

        return (
            <div className="container container-full" data-children="same-height">

                <div className="row">
                    <div className="col-sm-12">
                        <div className="custom-panel custom-panel-condensed light-gray-bg">
                            <div className="row row-condensed">
                                <div className="col-xl-5ths col-lg-4 col-md-6">
                                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                                         data-adjust="height">
                                        <h4 className="push-top-1 push-bot-2 text-center" data-type="title"><strong># of
                                            Women Age 30-40 Annually Diagnosed</strong></h4>
                                        <Line data={{
                                            labels: [1980,1985,1990,1995,2000,2005,2010,2015],
                                            datasets: [{
                                                    data: [200,230,260,290,320,350,380,410],
                                                    label: "Diagnosed",
                                                    borderColor: color_1,
                                                    fill: false
                                                }
                                            ]
                                        }} options={{
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
                                                        max: 500
                                                    }
                                                }]
                                            }
                                        }} width={400} height={400} />
                                    </div>
                                </div>
                                <div className="col-xl-5ths col-lg-4 col-md-6">
                                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                                         data-adjust="height">
                                        <h4 className="push-top-1 push-bot-2 text-center" data-type="title"><strong>ER+ /
                                            PR- / HER2- Annual Diagnoses</strong></h4>
                                        <Line data={{
                                            labels: [1980,1985,1990,1995,2000,2005,2010,2015],
                                            datasets: [{
                                                    data: [200,230,260,290,320,350,380,410],
                                                    label: "Diagnosed",
                                                    borderColor: color_1,
                                                    fill: false
                                                }
                                            ]
                                        }} options={{
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
                                                        max: 500
                                                    }
                                                }]
                                            }
                                        }} width={400} height={400} />
                                    </div>
                                </div>
                                <div className="col-xl-5ths col-lg-4 col-md-6">
                                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                                         data-adjust="height">
                                        <h4 className="push-top-1 push-bot-2 text-center" data-type="title"><strong>Breast
                                            Cancer by Grade and Size (Age 30-40)</strong></h4>
                                        <Bar data={{
                                            labels: ['Grade 1', 'Grade 2', 'Grade 3'],
                                            datasets: [{
                                                    data: [30,40,20],
                                                    // backgroundColor: gradient,
                                                    // hoverBackgroundColor: gradient
                                                }
                                            ]
                                        }} options={{
                                            legend: {
                                                display: false,
                                                position: 'bottom',
                                                labels: {
                                                    boxWidth: 10,
                                                    fontSize: 10,
                                                    padding: 8
                                                }
                                            }
                                        }} width={200} height={100} ref="chart" />
                                        <canvas id="breastCancer30_40_by_Size" width="200" height="100"></canvas>
                                    </div>
                                </div>
                                <div className="col-xl-5ths col-lg-4 col-md-6">
                                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                                         data-adjust="height">
                                        <h4 className="push-top-1 push-bot-2 text-center" data-type="title"><strong>Distribution
                                            of Stage of Cancer for Women Ages 30-40</strong></h4>
                                        <canvas id="breastCancer30_40_distribution" width="400" height="400"></canvas>
                                    </div>
                                </div>
                                <div className="col-xl-5ths col-lg-4 col-md-6">
                                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                                         data-adjust="height">
                                        <h4 className="push-top-1 push-bot-2 text-center" data-type="title"><strong>% of
                                            Women with Cancer by Race</strong></h4>
                                        <p className="no-margin pad-left-1 small"><strong>Overall</strong></p>
                                        <canvas id="breastCancer30_40_by_race_overall" width="200" height="75"></canvas>
                                        <p className="push-bot-0 push-top-3 pad-left-1 small"><strong>Within Your<br/>Age
                                            Bracket</strong></p>
                                        <canvas id="breastCancer30_40_by_race_within_your" width="200"
                                                height="75"></canvas>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="custom-panel custom-panel-condensed light-gray-bg push-bot-0">
                            <div className="row row-condensed">
                                <div className="col-xl-5ths col-lg-4 col-md-6">
                                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                                         data-adjust="height">
                                        <h4 className="push-top-1 push-bot-2 text-center" data-type="title"><strong>Surgery
                                            Decisions for Women Within Ages 30-40</strong></h4>
                                        <canvas id="breastCancer30_40_surgery_decision" width="400"
                                                height="400"></canvas>
                                    </div>
                                </div>
                                <div className="col-xl-5ths col-lg-4 col-md-6">
                                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                                         data-adjust="height">
                                        <h4 className="push-top-1 push-bot-2 text-center" data-type="title"><strong>Chemotherapy
                                            for Women Ages 30-40</strong></h4>
                                        <p className="no-margin pad-left-1 small"><strong>Overall</strong></p>
                                        <canvas id="breastCancer30_40_chemo_overall" width="200" height="75"></canvas>
                                        <p className="push-bot-0 push-top-3 pad-left-1 small"><strong>Breakout<br/>by Stage</strong>
                                        </p>
                                        <canvas id="breastCancer30_40_chemo_by_stage" width="200" height="75"></canvas>
                                    </div>
                                </div>
                                <div className="col-xl-5ths col-lg-4 col-md-6">
                                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                                         data-adjust="height">
                                        <h4 className="push-top-1 push-bot-2 text-center" data-type="title"><strong>Radiation
                                            for Women Ages 30-40</strong></h4>
                                        <p className="no-margin pad-left-1 small"><strong>Overall</strong></p>
                                        <canvas id="breastCancer30_40_radiation_overall" width="200"
                                                height="75"></canvas>
                                        <p className="push-bot-0 push-top-3 pad-left-1 small"><strong>Breakout<br/>by Stage</strong>
                                        </p>
                                        <canvas id="breastCancer30_40_radiation_by_stage" width="200"
                                                height="75"></canvas>
                                    </div>
                                </div>
                                <div className="col-xl-5ths col-lg-4 col-md-6">
                                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                                         data-adjust="height">
                                        <h4 className="push-top-1 push-bot-2 text-center" data-type="title"><strong>Survival
                                            Months for Women Ages 30-40</strong></h4>
                                        <canvas id="breastCancer30_40_survival_months" width="400"
                                                height="400"></canvas>
                                    </div>
                                </div>
                                <div className="col-xl-5ths col-lg-4 col-md-6">
                                    <div className="custom-panel custom-panel-condensed push-top-1 push-bot-0"
                                         data-adjust="height">
                                        <h4 className="push-top-1 push-bot-2 text-center" data-type="title"><strong>Cause of
                                            Death</strong></h4>
                                        <p className="no-margin pad-left-1 small"><strong>Overall</strong></p>
                                        <canvas id="breastCancer30_40_cause_death_overall" width="200"
                                                height="75"></canvas>
                                        <p className="push-bot-0 push-top-3 pad-left-1 small">
                                            <strong>Ages<br/>30-40</strong></p>
                                        <canvas id="breastCancer30_40_cause_death_30_40" width="200"
                                                height="75"></canvas>
                                    </div>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>

            </div>
        );
    }
}

const mapStateToProps = (state) => {
    return {
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(SpecificStatesView);
export {SpecificStatesView as SpecificStatesViewNotConnected};
