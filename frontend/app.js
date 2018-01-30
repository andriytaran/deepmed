import React from 'react';
import { connect } from 'react-redux';
import { push } from 'react-router-redux';
import classNames from 'classnames';
import PropTypes from 'prop-types';

import { authLogoutAndRedirect } from './actions/auth';
import './styles/style.scss';
import logo from './images/deep-med-logo-new.png';
import iconLogo from './images/icon-logo.png';
import avatar from './images/avatar.png';
import caretDown from './images/caret-down.png';
import Link from './components/Link';

class App extends React.Component {
    static propTypes = {
        isAuthenticated: PropTypes.bool.isRequired,
        children: PropTypes.shape().isRequired,
        isFetching: PropTypes.bool.isRequired,
        dispatch: PropTypes.func.isRequired,
        location: PropTypes.shape({
            pathname: PropTypes.string
        })
    };

    static defaultProps = {
        location: undefined
    };

    state = {
        spinnerCounter: 0
    };

    logout = () => {
        this.props.dispatch(authLogoutAndRedirect());
    };

    goToIndex = () => {
        this.props.dispatch(push('/'));
    };

    goToLogin = () => {
        this.props.dispatch(push('/login'));
    };

    goToDiagnosis = () => {
        this.props.dispatch(push('/diagnosis'));
    };

    goToNationalStates = () => {
        this.props.dispatch(push('/national-states'));
    };

    goToSpecificStates = () => {
        this.props.dispatch(push('/specific-states'));
    };

    goToSimilarDiagnoses = () => {
        this.props.dispatch(push('/similar-diagnoses'));
    };

    goToResources = () => {
        this.props.dispatch(push('/resources'));
    };

    componentDidMount() {
        this.timer = setInterval(() => {
            if (this.state.spinnerCounter === 3) {
                this.setState({
                    spinnerCounter: 0
                });
            } else {
                this.setState({
                    spinnerCounter: this.state.spinnerCounter + 1
                });
            }
        }, 2500);
    }

    componentWillUnmount() {
        clearInterval(this.timer);
    }

    render() {
        const isHome = this.props.location && this.props.location.pathname === '/';
        const spinnerTexts = ['DeepMed is analyzing  over 1M patient records and treatments',
            'DeepMed is processing patient records as far as back as 1973',
            'DeepMed is covering actual data from hospitals and oncology clinics',
            'DeepMed covers data spanning nearly 386 of the country from California to New Jersey'
        ];

        return (
            <div className="app">
                {this.props.isFetching ?
                    <div className="page-loader">
                        <div className="page-loader-sub-wrapper">
                            <div className="loader-spinner">
                                <div className="main">
                                    <div className="inside" />
                                </div>
                            </div>
                            <p className="push-top-3 text-lg" data-order="1">{spinnerTexts[this.state.spinnerCounter]}</p>
                        </div>
                    </div>
                    :
                    <div>
                        <nav className="sidebar active">
                            <div className="sidebar-header" style={{height: 56}}>
                                <Link onClick={() => {
                                    this.goToIndex();
                                }}>
                                    <img src={logo} width="136" height="auto" alt="presentation" style={{top: '15.5px'}} />
                                </Link>
                            </div>

                            { !isHome &&
                            <ul className="ul-no-bullets">
                                <li className={this.props.location && this.props.location.pathname === '/diagnosis' && 'active'}>
                                    <Link onClick={() => {
                                        this.goToDiagnosis();
                                    }}>
                                        <span className="icon-container">
                                            <i className="fa fa-heart-o"/>
                                        </span>
                                        Diagnosis
                                    </Link>
                                </li>
                                <li className={this.props.location && this.props.location.pathname === '/national-states' && 'active'}>
                                    <Link onClick={() => {
                                        this.goToNationalStates();
                                    }}>
                                        <span className="icon-container">
                                            <i className="fa fa-bar-chart"/>
                                        </span>
                                        National Stats
                                    </Link>
                                </li>
                                <li className={this.props.location && this.props.location.pathname === '/specific-states' && 'active'}>
                                    <Link onClick={() => {
                                        this.goToSpecificStates();
                                    }}>
                                        <span className="icon-container">
                                            <i className="fa fa-bar-chart"/>
                                        </span>
                                        Specific Stats
                                    </Link>
                                </li>
                                <li className={this.props.location && this.props.location.pathname === '/similar-diagnoses' && 'active'}>
                                    <Link onClick={() => {
                                        this.goToSimilarDiagnoses();
                                    }}>
                                        <span className="icon-container">
                                            <i className="fa fa-files-o"/>
                                        </span>
                                        Similar Diagnoses
                                    </Link>
                                </li>
                                <li className={this.props.location && this.props.location.pathname === '/resources' && 'active'}>
                                    <Link onClick={() => {
                                        this.goToResources();
                                    }}>
                                        <span className="icon-container">
                                            <i className="fa fa-laptop"/>
                                        </span>
                                        Resources
                                    </Link>
                                </li>
                            </ul>
                            }
                        </nav>
                        <div className="main-wrapper">
                            <nav className="navbar navbar-fixed-top">
                                <Link className="mobile-sidebar-trigger-container">
                                    <i className="icon-open-menu fa fa-bars"/>
                                    <i className="icon-close-menu fa fa-times"/>
                                </Link>
                                <div className="display-table display-table-100">
                                    <div className="display-table-cell pad-right-2">
                                        <div className="display-table">
                                            <div className="display-table-cell pad-right-2 hidden-md">
                                                <img src={iconLogo} width="50" height="auto"/>
                                            </div>
                                            <div className="display-table-cell hidden-sm">
                                                <h1 className="no-margin">#Page Location#</h1>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="display-table-cell text-right top-nav-tools">
                                        <div className="inline-block">
                                            <div className="display-table">
                                                <div className="display-table-cell pad-right-3">
                                                    <p className="inline-block">
                                                        <Link onClick={() => {
                                                        }} className="alerts-wrapper">
                                                            <span className="circle">
                                                                <span>12</span>
                                                            </span>
                                                            <i className="font-size-18 fa fa-bell-o"/>
                                                        </Link>
                                                    </p>
                                                </div>
                                                <div className="display-table-cell">
                                                    <div className="inline-block">
                                                        <div className="dropdown">
                                                            <Link href="javascript:void(0);"
                                                                className="dropdown-toggle user-dropdown inline-block"
                                                                data-toggle="dropdown"
                                                                id="userDropdownMenu">
                                                                <span className="avatar inline-block"
                                                                    style={{backgroundImage: avatar}} />
                                                                <img className="arrow"
                                                                    src={caretDown}
                                                                    width="10"
                                                                    height="auto"
                                                                    alt="presentation"
                                                                />
                                                            </Link>
                                                            <ul aria-labelledby="userDropdownMenu"
                                                                className="dropdown-menu dropdown-menu-right dropdown-menu-keep-open">
                                                                <li><Link onClick={() => {
                                                                }}>Menu Item 1</Link></li>
                                                                <li>
                                                                    <Link onClick={() => {
                                                                    }}>Menu Item 1</Link>
                                                                </li>
                                                                <li><Link onClick={() => {
                                                                    this.goToLogin();
                                                                }}>Log Out</Link></li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </nav>


                            <div className="content-wrapper">
                                <div className="container container-full text-center">
                                    <div className="row push-bot-3 hidden-md">
                                        <div className="col-md-12">
                                            <h1 className="no-margin">Thrax</h1>
                                            <p className="no-margin line-height-condensed text-light">
                                                Search
                                            </p>
                                        </div>
                                    </div>
                                </div>

                                {this.props.children}
                            </div>
                        </div>
                    </div>
                }
            </div>
        );
    }
}

const mapStateToProps = (state, ownProps) => {
    return {
        isAuthenticated: state.auth.isAuthenticated,
        location: state.routing.location,
        isFetching: state.diagnosis.isFetching
    };
};

export default connect(mapStateToProps)(App);
export { App as AppNotConnected };
