import React from 'react';
import {push} from 'react-router-redux';
import {connect} from 'react-redux';
import {Field, reduxForm} from 'redux-form';
import { bindActionCreators } from 'redux';
import PropTypes from 'prop-types';

import * as actionCreators from '../../actions/diagnosis';

import './style.scss';

class DiagnosisView extends React.Component {
    static propTypes = {
        isFetching: PropTypes.bool.isRequired,
        token: PropTypes.string.isRequired,
        dispatch: PropTypes.func.isRequired,
        actions: PropTypes.shape({
            submitDiagnosisData: PropTypes.func.isRequired
        }).isRequired
    };

    state = {
        showDetails: false
    };

    render() {
        return (
            <div className="container container-full">

                <div className="row">
                    <div className="col-md-12">
                        <div className="custom-panel custom-panel-condensed light-gray-bg">

                            <h2 className="push-top-2">Diagnosis</h2>

                            <form action="search-results.php" method="POST">

                                <div className="row row-condensed push-top-5 hidden-xs">
                                    <div className="col-sm-2 col-xs-6">
                                        <label>Age at Diagnosis</label>
                                    </div>
                                    <div className="col-sm-2 col-xs-6">
                                        <label>Tumor Size in mm</label>
                                    </div>
                                    <div className="col-sm-2 col-xs-6">
                                        <label>Tumor Grade</label>
                                    </div>
                                    <div className="col-sm-2 col-xs-6">
                                        <label># of Positive Nodes</label>
                                    </div>
                                    <div className="col-sm-2 col-xs-6">
                                        <label>ER Status</label>
                                    </div>
                                    <div className="col-sm-2 col-xs-6">
                                        <label>HER2 Status</label>
                                    </div>
                                </div>
                                <div className="row row-condensed push-top-2-xs">
                                    <div className="col-sm-2 col-xs-6">
                                        <label className="visible-xs">Age at Diagnosis</label>
                                        <input id="ageField" type="text" className="form-control text-input-sm"
                                               value="39"/>
                                    </div>
                                    <div className="col-sm-2 col-xs-6">
                                        <label className="visible-xs">Tumor Size in mm</label>
                                        <input type="text" className="form-control text-input-sm" value="16"/>
                                    </div>
                                    <div className="col-sm-2 col-xs-6 push-top-2-xs">
                                        <label className="visible-xs">Tumor Grade</label>
                                        <select className="form-control text-input-sm">
                                            <option>1 (Low)</option>
                                            <option>2 (Medium)</option>
                                            <option>3 (High)</option>
                                        </select>
                                    </div>
                                    <div className="col-sm-2 col-xs-6 push-top-2-xs">
                                        <label><span className="hidden-xs">Number</span><span
                                            className="visible-xs display-inline">#</span> of Positive Nodes</label>
                                        <select className="form-control text-input-sm">
                                            {Array.from(new Array(24), (val, index) => { return <option key={index} value={index + 1}>{index + 1}</option>; })}
                                        </select>
                                    </div>
                                    <div className="col-sm-2 col-xs-6 push-top-2-xs">
                                        <label className="visible-xs">ER Status</label>
                                        <select className="form-control text-input-sm">
                                            <option>Positive</option>
                                            <option>Negative</option>
                                        </select>
                                    </div>
                                    <div className="col-sm-2 col-xs-6 push-top-2-xs">
                                        <label className="visible-xs">HER2 Status</label>
                                        <select className="form-control text-input-sm">
                                            <option>Positive</option>
                                            <option>Negative</option>
                                        </select>
                                    </div>
                                </div>
                                <div className="row row-condensed push-top-3 hidden-xs">
                                    <div className="col-sm-2 col-xs-6">
                                        <label>PR Status</label>
                                    </div>
                                    <div className="col-sm-2 col-xs-6">
                                        <label>Ethnicity (optional)</label>
                                    </div>
                                    <div className="col-sm-2 col-xs-6">
                                        <label>Stage</label>
                                    </div>
                                    <div className="col-sm-2 col-xs-6">
                                        <label>Site</label>
                                    </div>
                                    <div className="col-sm-2 col-xs-6">
                                        <label>Laterailty</label>
                                    </div>
                                    <div className="col-sm-2 col-xs-6">
                                        <label>Type</label>
                                    </div>
                                </div>

                                <div className="row row-condensed push-top-2-xs">
                                    <div className="col-sm-2 col-xs-6">
                                        <label className="visible-xs">PR Status</label>
                                        <select className="form-control text-input-sm">
                                            <option>Positive</option>
                                            <option>Negative</option>
                                        </select>
                                    </div>
                                    <div className="col-sm-2 col-xs-6">
                                        <label className="visible-xs">Ethnicity (optional)</label>
                                        <select className="form-control text-input-sm">
                                            <option>African-American</option>
                                            <option>Asian</option>
                                            <option>Native American</option>
                                            <option>Caucasian</option>
                                        </select>
                                    </div>
                                    <div className="col-sm-2 col-xs-6 push-top-2-xs">
                                        <label className="visible-xs">Stage</label>
                                        <select className="form-control text-input-sm">
                                            <option>Optional</option>
                                            <option>Stage 1</option>
                                            <option>Stage 2</option>
                                            <option>Stage 3</option>
                                        </select>
                                    </div>
                                    <div className="col-sm-2 col-xs-6 push-top-2-xs">
                                        <label className="visible-xs">Breadth</label>
                                        <select className="form-control text-input-sm">
                                            <option>Optional</option>
                                            <option>Option a</option>
                                            <option>Option b</option>
                                            <option>Option c</option>
                                        </select>
                                    </div>
                                    <div className="col-sm-2 col-xs-6 push-top-2-xs">
                                        <label className="visible-xs">Laterailty</label>
                                        <select className="form-control text-input-sm">
                                            <option>Optional</option>
                                            <option>Option a</option>
                                            <option>Option b</option>
                                            <option>Option c</option>
                                        </select>
                                    </div>
                                    <div className="col-sm-2 col-xs-6 push-top-2-xs">
                                        <label className="visible-xs">Type</label>
                                        <select className="form-control text-input-sm">
                                            <option>Optional</option>
                                            <option>Option a</option>
                                            <option>Option b</option>
                                            <option>Option c</option>
                                        </select>
                                    </div>
                                </div>

                            </form>
                        </div>

                        <div className="custom-panel custom-panel-condensed light-gray-bg push-bot-0">

                            <h2 className="push-top-2">Recommended Treatment Plans</h2>

                            <div className="push-top-5">
                                <div
                                    className="custom-panel custom-panel-condensed custom-panel-no-vertical-pad no-border bg-transparent push-bot-0">
                                    <p className="push-top-0 push-bot-1"><strong>Overall Plans</strong></p>
                                </div>
                                <div className="custom-panel custom-panel-condensed push-bot-0">
                                    <table
                                        className="table table-responsive table-middle-cell-align table-hover tablesaw tablesaw-stack"
                                        data-tablesaw-mode="stack">
                                        <thead>
                                        <tr>
                                            <th><h6>TREATMENT PLANS</h6></th>
                                            <th><h6>CONFIDENCE LEVEL</h6></th>
                                            <th><h6>SURGERY</h6></th>
                                            <th><h6>SURGERY TYPE</h6></th>
                                            <th><h6>RADIATION</h6></th>
                                            <th><h6>CHEMO</h6></th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        <tr>
                                            <td><p className="no-margin">Preferred Outcome A</p></td>
                                            <td><p className="no-margin">82%</p></td>
                                            <td><p className="no-margin">Y</p></td>
                                            <td><p className="no-margin">Lumpectomy</p></td>
                                            <td><p className="no-margin">Yes</p></td>
                                            <td><p className="no-margin">Yes</p></td>
                                        </tr>
                                        <tr>
                                            <td><p className="no-margin">Preferred Outcome B</p></td>
                                            <td><p className="no-margin">47%</p></td>
                                            <td><p className="no-margin">Y</p></td>
                                            <td><p className="no-margin">Mastectomy</p></td>
                                            <td><p className="no-margin">No</p></td>
                                            <td><p className="no-margin">Yes</p></td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                            <div className="push-top-5">
                                <div
                                    className="custom-panel custom-panel-condensed custom-panel-no-vertical-pad no-border bg-transparent push-bot-0">
                                    <p className="push-top-0 push-bot-1"><strong>Chemotherapy</strong></p>
                                </div>
                                <div className="custom-panel custom-panel-condensed push-bot-0">
                                    <table
                                        className="table table-responsive table-middle-cell-align table-equal-width-3 table-hover tablesaw tablesaw-stack"
                                        data-tablesaw-mode="stack">
                                        <thead>
                                        <tr>
                                            <th><h6>CHEMO TREATMENT PLANS</h6></th>
                                            <th><h6>NUMBER OF TREATMENTS</h6></th>
                                            <th><h6>ADMINISTRATION</h6></th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        <tr>
                                            <td><p className="no-margin"><span
                                                className="number-circle blue-circle">1</span> AC + T</p></td>
                                            <td>
                                                <table>
                                                    <tr>
                                                        <td>
                                                            <p className="push-bot-1 push-top-1">A) 4AC, 4T</p>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>
                                                            <p className="push-bot-1 push-top-1">B) 4AC, 12T</p>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                            <td>
                                                <table>
                                                    <tr>
                                                        <td>
                                                            <p className="no-margin">A)</p>
                                                        </td>
                                                        <td className="pad-left-1 pad-right-1">
                                                            <p className="no-margin">AC</p>
                                                            <p className="push-bot-1 line-height-condensed small">
                                                                <small>Every 2 weeks</small>
                                                            </p>
                                                        </td>
                                                        <td className="vertical-line"></td>
                                                        <td className="pad-left-2">
                                                            <p className="no-margin">T</p>
                                                            <p className="push-bot-1 line-height-condensed small">
                                                                <small>Every 2 weeks</small>
                                                            </p>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td>
                                                            <p className="no-margin">B)</p>
                                                        </td>
                                                        <td className="pad-left-1 pad-right-1">
                                                            <p className="push-top-1">AC</p>
                                                            <p className="no-margin line-height-condensed small">
                                                                <small>Every 2 weeks</small>
                                                            </p>
                                                        </td>
                                                        <td className="vertical-line"></td>
                                                        <td className="pad-left-2">
                                                            <p className="push-top-1">T</p>
                                                            <p className="no-margin line-height-condensed small">
                                                                <small>Every week</small>
                                                            </p>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td><p className="no-margin"><span
                                                className="number-circle blue-circle">2</span> FEC</p></td>
                                            <td><p className="no-margin">3 FEC</p></td>
                                            <td><p className="no-margin">Every 3 weeks</p></td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                            <div className="push-top-5">
                                <div
                                    className="custom-panel custom-panel-condensed custom-panel-no-vertical-pad no-border bg-transparent push-bot-0">
                                    <p className="push-top-0 push-bot-1"><strong>Radiation Therapy</strong></p>
                                </div>
                                <div className="custom-panel custom-panel-condensed push-bot-0">
                                    <table
                                        className="table table-responsive table-middle-cell-align table-equal-width-3 table-hover tablesaw tablesaw-stack"
                                        data-tablesaw-mode="stack">
                                        <thead>
                                        <tr>
                                            <th><h6>RADIATION TREATMENT PLANS</h6></th>
                                            <th><h6>NUMBER OF TREATMENTS</h6></th>
                                            <th><h6>ADMINISTRATION</h6></th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        <tr>
                                            <td><p className="no-margin"><span
                                                className="number-circle blue-circle">1</span> Beam Radiation</p></td>
                                            <td><p className="no-margin">30</p></td>
                                            <td><p className="no-margin">Daily</p></td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                            <div className="push-top-5">
                                <div
                                    className="custom-panel custom-panel-condensed custom-panel-no-vertical-pad no-border bg-transparent push-bot-0">
                                    <p className="push-top-0 push-bot-1"><strong>Hormonal Therapy</strong></p>
                                </div>
                                <div className="custom-panel custom-panel-condensed push-bot-0">
                                    <table
                                        className="table table-responsive table-middle-cell-align table-equal-width-3 table-hover tablesaw tablesaw-stack"
                                        data-tablesaw-mode="stack">
                                        <thead>
                                        <tr>
                                            <th><h6>HORMONAL TREATMENT PLANS</h6></th>
                                            <th><h6>NUMBER OF TREATMENTS</h6></th>
                                            <th><h6>ADMINISTRATION</h6></th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        <tr>
                                            <td><p className="no-margin"><span
                                                className="number-circle blue-circle">1</span> Tamoxifen</p></td>
                                            <td><p className="no-margin">120</p></td>
                                            <td><p className="no-margin">Monthly</p></td>
                                        </tr>
                                        </tbody>
                                    </table>
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
        isFetching: state.diagnosis.isFetching
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        actions: bindActionCreators(actionCreators, dispatch)
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(DiagnosisView);
export { DiagnosisView as DiagnosisViewNotConnected };
