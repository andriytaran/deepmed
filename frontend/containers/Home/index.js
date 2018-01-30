import React from 'react';
import {push} from 'react-router-redux';
import {connect} from 'react-redux';
import { bindActionCreators } from 'redux';
import PropTypes from 'prop-types';

import * as actionCreators from '../../actions/diagnosis';

import './style.scss';
import DiagnosisForm from '../../forms/DiagnosisForm';

class HomeView extends React.Component {
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
            <div className="container container-full text-center">
                <div className="row">
                    <div className="col-md-12">
                        <div className="custom-panel custom-panel-md transparent-bg no-border push-bot-0">
                            <h2 className="no-margin">Feel free to list your conditions and let us figure it out or
                                use
                                Advanced Search to input your diagnosis in detail.</h2>
                        </div>
                    </div>
                </div>

                <div className="row">
                    <div className="col-md-12">
                        <div className="custom-panel custom-panel-md light-gray-bg">
                            <DiagnosisForm
                                showDetails={this.state.showDetails}
                                onShowDetails={(show) => {
                                    this.setState({showDetails: show});
                                }}
                                onSubmit={(values) => {
                                    this.props.actions.submitDiagnosisData(this.props.token, values);
                                }}
                            />
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

export default connect(mapStateToProps, mapDispatchToProps)(HomeView);
export { HomeView as HomeViewNotConnected };
