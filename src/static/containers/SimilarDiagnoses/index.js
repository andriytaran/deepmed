import React from 'react';
import {push} from 'react-router-redux';
import {connect} from 'react-redux';
import {Field, reduxForm} from 'redux-form';
import {bindActionCreators} from 'redux';
import PropTypes from 'prop-types';

import { Line, Bar, Pie, HorizontalBar } from 'react-chartjs-2';

import './style.scss';

class SimilarDiagnosesView extends React.Component {
    static propTypes = {
        token: PropTypes.string.isRequired,
        dispatch: PropTypes.func.isRequired,
    };

    state = {
        showDetails: false
    };

    render() {
        const data = [{'age': 38,
            'ethnicity': 'Asian Am.',
            'tumor_size': 2.1,
            'tumor_grade': 3,
            'er_status': '+',
            'pr_status': '+',
            'her2': '-',
            'laterality': 'L',
            'site': 'Upper Outer',
            'type': 'IDC',
            'stage': 'IIB',
            'nodes': 3,
            'surgery': 'Bi Lat  Mastectomy',
            'chemo': 'Yes',
            'radiation': 'No',
            'year': 2012,
            'months': 63,
            'cod': 'Other'}, {'age': 38,
            'ethnicity': 'Asian Am.',
            'tumor_size': 2.1,
            'tumor_grade': 3,
            'er_status': '+',
            'pr_status': '+',
            'her2': '-',
            'laterality': 'L',
            'site': 'Upper Outer',
            'type': 'IDC',
            'stage': 'IIB',
            'nodes': 3,
            'surgery': 'Bi Lat  Mastectomy',
            'chemo': 'Yes',
            'radiation': 'No',
            'year': 2012,
            'months': 63,
            'cod': 'Other'}, {'age': 38,
            'ethnicity': 'Asian Am.',
            'tumor_size': 2.1,
            'tumor_grade': 3,
            'er_status': '+',
            'pr_status': '+',
            'her2': '-',
            'laterality': 'L',
            'site': 'Upper Outer',
            'type': 'IDC',
            'stage': 'IIB',
            'nodes': 3,
            'surgery': 'Bi Lat  Mastectomy',
            'chemo': 'Yes',
            'radiation': 'No',
            'year': 2012,
            'months': 63,
            'cod': 'Other'}, {'age': 38,
            'ethnicity': 'Asian Am.',
            'tumor_size': 2.1,
            'tumor_grade': 3,
            'er_status': '+',
            'pr_status': '+',
            'her2': '-',
            'laterality': 'L',
            'site': 'Upper Outer',
            'type': 'IDC',
            'stage': 'IIB',
            'nodes': 3,
            'surgery': 'Bi Lat  Mastectomy',
            'chemo': 'Yes',
            'radiation': 'No',
            'year': 2012,
            'months': 63,
            'cod': 'Other'}, {'age': 38,
            'ethnicity': 'Asian Am.',
            'tumor_size': 2.1,
            'tumor_grade': 3,
            'er_status': '+',
            'pr_status': '+',
            'her2': '-',
            'laterality': 'L',
            'site': 'Upper Outer',
            'type': 'IDC',
            'stage': 'IIB',
            'nodes': 3,
            'surgery': 'Bi Lat  Mastectomy',
            'chemo': 'Yes',
            'radiation': 'No',
            'year': 2012,
            'months': 63,
            'cod': 'Other'}];
        
        return (
            <div className="container container-full" data-children="same-height">

                <div className="row">

                    <div className="col-md-12">
                        <div className="custom-panel custom-panel-condensed push-bot-0">
                            <div className="scroll-y scroll-x max-height-700">
                                <table className="table table-responsive table-middle-cell-align table-hover">
                                    <thead>
                                    <tr>
                                        <th colSpan="4">
                                            <h5 className="text-center">Diagnosis</h5>
                                        </th>
                                        <th colSpan="3">
                                            <h5 className="text-center">Status</h5>
                                        </th>
                                        <th colSpan="5">
                                        </th>
                                        <th colSpan="3">
                                            <h5 className="text-center">Treatment</h5>
                                        </th>
                                        <th colSpan="3">
                                            <h5 className="text-center">Outcome</h5>
                                        </th>
                                    </tr>
                                    <tr>
                                        <th><h6 className="push-top-1">Age</h6></th>
                                        <th><h6 className="push-top-1">Ethnicity</h6></th>
                                        <th><h6 className="push-top-1">Size</h6></th>
                                        <th><h6 className="push-top-1">Grade</h6></th>
                                        <th><h6 className="push-top-1">ER</h6></th>
                                        <th><h6 className="push-top-1">PR</h6></th>
                                        <th><h6 className="push-top-1">HER2</h6></th>
                                        <th><h6 className="push-top-1">Lat</h6></th>
                                        <th><h6 className="push-top-1">Site</h6></th>
                                        <th><h6 className="push-top-1">Type</h6></th>
                                        <th><h6 className="push-top-1">Stage</h6></th>
                                        <th><h6 className="push-top-1">+Nodes</h6></th>

                                        <th><h6 className="push-top-1">Surgery</h6></th>
                                        <th><h6 className="push-top-1">Chemo</h6></th>
                                        <th><h6 className="push-top-1">Radiation</h6></th>
                                        <th><h6 className="push-top-1">Year Dx</h6></th>
                                        <th><h6 className="push-top-1">Survival Mos.</h6></th>
                                        <th><h6 className="push-top-1">CoD</h6></th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {
                                        data.map((item) => {
                                            return (<tr>
                                                    <td><p className="no-margin">{item['age']}</p></td>
                                                    <td><p className="no-margin">{item['ethnicity']}</p></td>
                                                    <td><p className="no-margin">{item['tumor_size']}</p></td>
                                                    <td><p className="no-margin">{item['tumor_grade']}</p></td>
                                                    <td><p className="no-margin">{item['er_status']}</p></td>
                                                    <td><p className="no-margin">{item['pr_status']}</p></td>
                                                    <td><p className="no-margin">{item['her2']}</p></td>
                                                    <td><p className="no-margin">{item['laterality']}</p></td>
                                                    <td><p className="no-margin">{item['site']}</p></td>
                                                    <td><p className="no-margin">{item['type']}</p></td>
                                                    <td><p className="no-margin">{item['stage']}</p></td>
                                                    <td><p className="no-margin">{item['nodes']}</p></td>
                                                    <td><p className="no-margin">{item['surgery']}</p></td>
                                                    <td><p className="no-margin">{item['chemo']}</p></td>
                                                    <td><p className="no-margin">{item['radiation']}</p></td>
                                                    <td><p className="no-margin">{item['year']}</p></td>
                                                    <td><p className="no-margin">{item['months']}</p></td>
                                                    <td><p className="no-margin">{item['cod']}</p></td>
                                                </tr>);
                                        })
                                    }
                                    </tbody>
                                </table>
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

export default connect(mapStateToProps, mapDispatchToProps)(SimilarDiagnosesView);
export {SimilarDiagnosesView as SimilarDiagnosesViewNotConnected};
