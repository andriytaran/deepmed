import React from 'react';
import {push} from 'react-router-redux';
import {connect} from 'react-redux';
import {Field, reduxForm} from 'redux-form';
import {bindActionCreators} from 'redux';
import PropTypes from 'prop-types';

import { Line } from 'react-chartjs-2';

import './style.scss';

class NationalStatesView extends React.Component {
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

        return (
            <div className="container container-full" data-children="same-height">

                <div className="row">
                    <div className="col-md-6">
                        <div className="custom-panel custom-panel-condensed light-gray-bg" data-adjust="height">

                            <h2 className="no-margin text-center">Breast Cancer by State</h2>

                            <div className="text-center">
                                <div id="map" style={{width: '100%', height: 400}}></div>
                            </div>

                            <div className="row push-top-5">
                                <div className="col-md-12 text-center">
                                    <div
                                        className="custom-panel custom-panel-condensed gray-bg inline-block  push-bot-0 text-left">
                                        <p className="no-margin">Range:</p>
                                        <div className="push-top-1">
                                            <div className="display-table">
                                                <div className="display-table-cell">
                                                    <div className="display-table-cell">
                                                        <span className="range-square"
                                                              style={{backgroundColor: '#47cfd1'}}></span>
                                                    </div>
                                                    <div className="display-table-cell">
                                                        <p className="no-margin line-height-100 small">&nbsp;106.6 to
                                                            118.3</p>
                                                    </div>
                                                </div>
                                                <div className="display-table-cell pad-left-1">
                                                    <div className="display-table-cell">
                                                        <span className="range-square"
                                                              style={{backgroundColor: '#04a9a9'}}></span>
                                                    </div>
                                                    <div className="display-table-cell">
                                                        <p className="no-margin line-height-100 small">&nbsp;118.7 to
                                                            125.5</p>
                                                    </div>
                                                </div>
                                                <div className="display-table-cell pad-left-1">
                                                    <div className="display-table-cell">
                                                        <span className="range-square"
                                                              style={{backgroundColor: '#48ccf5'}}></span>
                                                    </div>
                                                    <div className="display-table-cell">
                                                        <p className="no-margin line-height-100 small">&nbsp;125.9 to
                                                            132.0</p>
                                                    </div>
                                                </div>
                                                <div className="display-table-cell pad-left-1">
                                                    <div className="display-table-cell">
                                                        <span className="range-square"
                                                              style={{backgroundColor: '#77c2d9'}}></span>
                                                    </div>
                                                    <div className="display-table-cell">
                                                        <p className="no-margin line-height-100 small">&nbsp;132.3 to
                                                            144.9</p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                        </div>
                    </div>

                    <div className="col-md-6">
                        <div className="custom-panel custom-panel-condensed light-gray-bg" data-adjust="height">

                            <h2 className="no-margin text-center">Breast Cancer at a Glance</h2>
                            <div className="custom-panel custom-panel-condensed push-top-4">
                                <div className="row row-condensed">
                                    <div className="col-sm-12">
                                        <p className="push-top-1 push-bot-2 text-center"><strong>Number per 100,000
                                            females</strong></p>
                                        <Line data={{
                                            labels: [1192,1995,1998,2001,2004,2007,2010,2014],
                                            datasets: [{
                                                    data: [50,49,48,47,46,45,44,43,42,41],
                                                    label: "Deaths",
                                                    borderColor: color_1,
                                                    fill: false
                                                }, {
                                                    data: [147,144,148,142,149,147,145,140,146,147],
                                                    label: "New Cases",
                                                    borderColor: color_3,
                                                    fill: false
                                                }
                                            ]
                                        }} options={{
                                            legend: {
                                                display: false,
                                                position: 'bottom'
                                            }
                                        }} width={500} height={100} />
                                    </div>
                                </div>
                                <div className="row row-condensed push-top-2">
                                    <div className="col-sm-6">
                                        <div className="custom-panel custom-panel-condensed no border green-bg push-bot-0">
                                            <div className="display-table display-table-100">
                                                <div className="display-table-cell">
                                                    <p className="no-margin text-white small">
                                                        Estimated New<br/>Cases in 2017
                                                    </p>
                                                </div>
                                                <div className="display-table-cell text-right">
                                                    <p className="no-margin text-white">
                                                        <strong>252,719</strong>
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                        <div className="custom-panel custom-panel-condensed no border green-bg push-bot-0">
                                            <div className="display-table display-table-100">
                                                <div className="display-table-cell">
                                                    <p className="no-margin text-white small">
                                                        % of All New<br/>Cancer Cases
                                                    </p>
                                                </div>
                                                <div className="display-table-cell text-right">
                                                    <p className="no-margin text-white">
                                                        <strong>15.0%</strong>
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="col-sm-6">
                                        <div className="custom-panel custom-panel-condensed no border blue-bg push-bot-0">
                                            <div className="display-table display-table-100">
                                                <div className="display-table-cell">
                                                    <p className="no-margin text-white small">
                                                        Estimated<br/>Deaths in 2017
                                                    </p>
                                                </div>
                                                <div className="display-table-cell text-right">
                                                    <p className="no-margin text-white">
                                                        <strong>40,610</strong>
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                        <div className="custom-panel custom-panel-condensed no border blue-bg push-bot-0">
                                            <div className="display-table display-table-100">
                                                <div className="display-table-cell">
                                                    <p className="no-margin text-white small">
                                                        % of All<br/>Cancer Deaths
                                                    </p>
                                                </div>
                                                <div className="display-table-cell text-right">
                                                    <p className="no-margin text-white">
                                                        <strong>6.8%</strong>
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div className="custom-panel custom-panel-condensed push-bot-0">
                                <div className="display-table">
                                    <div className="display-table-cell display-block-xs">
                                        <div
                                            className="custom-panel custom-panel-condensed gradient-bg text-center push-bot-0">
                                            <p className="no-margin text-white"><strong>Percent<br/>Surviving 5</strong></p>
                                            <p className="font-size-40 push-top-1 push-bot-1 text-white">
                                                <strong>89.7%</strong></p>
                                            <p className="no-margin text-white text-light">2017-2013</p>
                                        </div>
                                    </div>
                                    <div className="display-table-cell display-block-xs push-top-2-xs pad-left-1">
                                        <p className="push-bot-1">
                                            Number of New Cases and Deaths per 100,00: The number of new cases of female
                                            breast... <a href="#">Read more</a>
                                        </p>
                                        <p className="push-bot-1">
                                            Lifetime Risk of Developing Cancer: Aproximately 12.4 percent of women will
                                            be... <a href="#">Read more</a>
                                        </p>
                                        <p>
                                            Prevalence of This Cancer: in 2014, there were an estimated 3,327,552
                                            women... <a href="#">Read more</a>
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="row">
                    <div className="col-sm-12">
                        <div className="custom-panel custom-panel-condensed light-gray-bg">

                            <h2 className="no-margin text-center">Breast Cancer by Age</h2>

                            <div className="row push-top-4">
                                <div className="col-md-6">
                                    <div className="custom-panel custom-panel-condensed push-bot-0">
                                        <p className="push-top-1 push-bot-2 text-center"><strong>Age-Specific Rates of
                                            Breast Cancer in the United States</strong></p>
                                        <Line data={{
                                            labels: ['0-14','15-19', '20-14', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85'],
                                            datasets: [{
                                                    data: [7,14,20,248,70,148,190,200,250,300,350,400,450,450,400,350,300],
                                                    label: "Deaths",
                                                    borderColor: color_1,
                                                    fill: false
                                                }
                                            ]
                                        }} options={{
                                            legend: {
                                                display: false,
                                                position: 'bottom'
                                            }
                                        }} width={275} height={100} />
                                    </div>
                                </div>
                                <div className="col-md-6 push-top-1-sm">
                                    <div className="custom-panel custom-panel-condensed push-bot-0">
                                        <p className="push-top-1 push-bot-2 text-center"><strong>Percent of U.S. Women Who
                                            Develop CancerAccording to o Their Age (2010-2012)</strong></p>
                                        <div className="custom-panel custom-panel-condensed light-gray-bg push-bot-0">
                                            <table className="table table-responsive table-middle-cell-align table-hover">
                                                <thead>
                                                <tr>
                                                    <th><h6>CURRENT AGE</h6></th>
                                                    <th><h6>10 YEARS</h6></th>
                                                    <th><h6>20 YEARS</h6></th>
                                                    <th><h6>30 YEARS</h6></th>
                                                </tr>
                                                </thead>
                                                <tbody>
                                                <tr>
                                                    <td><p className="no-margin">30</p></td>
                                                    <td><p className="no-margin">0.44</p></td>
                                                    <td><p className="no-margin">1.87</p></td>
                                                    <td><p className="no-margin">4.05</p></td>
                                                </tr>
                                                <tr>
                                                    <td><p className="no-margin">40</p></td>
                                                    <td><p className="no-margin">1.44</p></td>
                                                    <td><p className="no-margin">3.65</p></td>
                                                    <td><p className="no-margin">6.80</p></td>
                                                </tr>
                                                <tr>
                                                    <td><p className="no-margin">50</p></td>
                                                    <td><p className="no-margin">2.28</p></td>
                                                    <td><p className="no-margin">5.53</p></td>
                                                    <td><p className="no-margin">8.75</p></td>
                                                </tr>
                                                <tr>
                                                    <td><p className="no-margin">60</p></td>
                                                    <td><p className="no-margin">3.46</p></td>
                                                    <td><p className="no-margin">6.89</p></td>
                                                    <td><p className="no-margin">8.89</p></td>
                                                </tr>
                                                <tr>
                                                    <td><p className="no-margin">70</p></td>
                                                    <td><p className="no-margin">3.89</p></td>
                                                    <td><p className="no-margin">6.16</p></td>
                                                    <td><p className="no-margin">N/A</p></td>
                                                </tr>

                                                </tbody>
                                            </table>
                                        </div>
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

export default connect(mapStateToProps, mapDispatchToProps)(NationalStatesView);
export {NationalStatesView as NationalStatesViewNotConnected};
