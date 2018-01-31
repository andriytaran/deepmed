import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './Layout.css'
import globalStyles from '../../styles/style.scss'
import {Link} from '../../components'
import {
  DIAGNOSIS_ROUTE,
  HOME_ROUTE,
  LOGOUT_ROUTE,
  NATIONAL_STATES_ROUTE,
  RESOURCES_ROUTE,
  SIMILAR_DIAGNOSES_ROUTE,
  SPECIFIC_STATES_ROUTE
} from '../../routes/index'
import cn from 'classnames'

class AppLayout extends React.Component {
  state = {
    spinnerCounter: 0
  }

  componentDidMount() {
    this.timer = setInterval(() => {
      if (this.state.spinnerCounter === 3) {
        this.setState({
          spinnerCounter: 0
        })
      } else {
        this.setState({
          spinnerCounter: this.state.spinnerCounter + 1
        })
      }
    }, 2500)
  }

  componentWillUnmount() {
    clearInterval(this.timer)
  }

  render() {
    const {currentRouteName, loading} = this.props
    const spinnerTexts = [
      'DeepMed is analyzing  over 1M patient records and treatments',
      'DeepMed is processing patient records as far as back as 1973',
      'DeepMed is covering actual data from hospitals and oncology clinics',
      'DeepMed covers data spanning nearly 386 of the country from California to New Jersey'
    ]

    return (
      <div className="app">
        {loading ?
          <div className="page-loader">
            <div className="page-loader-sub-wrapper">
              <div className="loader-spinner">
                <div className="main">
                  <div className="inside"/>
                </div>
              </div>
              <p className="push-top-3 text-lg" data-order="1">{spinnerTexts[this.state.spinnerCounter]}</p>
            </div>
          </div>
          :
          <div>
            <nav className="sidebar active">
              <div className="sidebar-header" style={{height: 56}}>
                <Link to={HOME_ROUTE}>
                  <img src={require('../../static/deep-med-logo-new.png')} width="136" height="auto" alt="presentation"
                       style={{top: '15.5px'}}/>
                </Link>
              </div>
              <ul className="ul-no-bullets">
                <li className={cn(currentRouteName === DIAGNOSIS_ROUTE && 'active')}>
                  <Link to={DIAGNOSIS_ROUTE}>
                <span className="icon-container">
                <i className="fa fa-heart-o"/>
                </span>
                    Diagnosis
                  </Link>
                </li>
                <li className={cn(currentRouteName === NATIONAL_STATES_ROUTE && 'active')}>
                  <Link to={NATIONAL_STATES_ROUTE}>
                <span className="icon-container">
                <i className="fa fa-bar-chart"/>
                </span>
                    National Stats
                  </Link>
                </li>
                <li className={cn(currentRouteName === SPECIFIC_STATES_ROUTE && 'active')}>
                  <Link to={SPECIFIC_STATES_ROUTE}>
                <span className="icon-container">
                <i className="fa fa-bar-chart"/>
                </span>
                    Specific Stats
                  </Link>
                </li>
                <li
                  className={cn(currentRouteName === SIMILAR_DIAGNOSES_ROUTE && 'active')}>
                  <Link to={SIMILAR_DIAGNOSES_ROUTE}>
                <span className="icon-container">
                <i className="fa fa-files-o"/>
                </span>
                    Similar Diagnoses
                  </Link>
                </li>
                <li className={cn(currentRouteName === RESOURCES_ROUTE && 'active')}>
                  <Link to={RESOURCES_ROUTE}>
                <span className="icon-container">
                <i className="fa fa-laptop"/>
                </span>
                    Resources
                  </Link>
                </li>
              </ul>
            </nav>
            <div className="main-wrapper">
              <nav className="navbar navbar-fixed-top">
                <a className="mobile-sidebar-trigger-container">
                  <i className="icon-open-menu fa fa-bars"/>
                  <i className="icon-close-menu fa fa-times"/>
                </a>
                <div className="display-table display-table-100">
                  <div className="display-table-cell pad-right-2">
                    <div className="display-table">
                      <div className="display-table-cell pad-right-2 hidden-md">
                        <img src={require('../../static/icon-logo.png')} width="50" height="auto"/>
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
                            <a className="alerts-wrapper">
                              <span className="circle">
                                <span>12</span>
                              </span>
                              <i className="font-size-18 fa fa-bell-o"/>
                            </a>
                          </p>
                        </div>
                        <div className="display-table-cell">
                          <div className="inline-block">
                            <div className="dropdown">
                              <a
                                className="dropdown-toggle user-dropdown inline-block"
                                data-toggle="dropdown"
                                id="userDropdownMenu"
                              >
                                <span className="avatar inline-block"
                                      style={{backgroundImage: require('../../static/avatar.png')}}/>
                                <img className="arrow"
                                     src={require('../../static/caret-down.png')}
                                     width="10"
                                     height="auto"
                                     alt="presentation"
                                />
                              </a>
                              <ul aria-labelledby="userDropdownMenu"
                                  className="dropdown-menu dropdown-menu-right dropdown-menu-keep-open">
                                <li>
                                  <a>Menu Item 1</a></li>
                                <li>
                                  <a>Menu Item 1</a>
                                </li>
                                <li>
                                  <Link to={LOGOUT_ROUTE}>Log Out</Link>
                                </li>
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
    )
  }
}


const mapState = state => ({
  loggedIn: state.user.loggedIn,
  currentRouteName: state.global.currentRouteName,
  loading: state.diagnosis.loading,
})

const mapDispatch = {}

export default connect(mapState, mapDispatch)(withStyles(
  globalStyles,
  s,
)(AppLayout))