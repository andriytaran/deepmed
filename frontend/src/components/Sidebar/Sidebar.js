import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './Sidebar.css'
import {Link} from '../../components'
import {
  CUSTOM_ANALYTICS_ROUTE,
  DIAGNOSIS_ROUTE,
  HOME_ROUTE,
  LOGIN_ROUTE,
  NATIONAL_STATES_ROUTE,
  RESOURCES_ROUTE,
  SIMILAR_DIAGNOSES_ROUTE,
  SPECIFIC_STATES_ROUTE,
  USER_ROUTE,
} from '../../routes'
import cn from 'classnames'
import FaHeaderO from 'react-icons/lib/fa/heart-o'
import FaBarChart from 'react-icons/lib/fa/bar-chart'
import FaFileO from 'react-icons/lib/fa/file-o'
import FaLaptop from 'react-icons/lib/fa/laptop'

const MENU = [
  {routeName: DIAGNOSIS_ROUTE, label: 'Diagnosis', iconComponent: FaHeaderO},
  {routeName: NATIONAL_STATES_ROUTE, label: 'National Statistics', iconComponent: FaBarChart},
  {routeName: SPECIFIC_STATES_ROUTE, label: 'Individual Statistics', iconComponent: FaBarChart},
  {routeName: CUSTOM_ANALYTICS_ROUTE, label: 'Custom Analytics', iconComponent: FaBarChart},
  {routeName: SIMILAR_DIAGNOSES_ROUTE, label: 'Similar Diagnoses', iconComponent: FaFileO},
  {routeName: RESOURCES_ROUTE, label: 'Resources', iconComponent: FaLaptop},
]

class Sidebar extends React.Component {
  render() {
    const {sidebarOpened, currentRouteName} = this.props
    return (
      <nav className={cn(s.sidebar, sidebarOpened && s.opened)}>
        <Link to={HOME_ROUTE} className={s.logoWrapper}>
          <img
            className={s.logo}
            src={require('../../static/deep-med-logo-new.png')}
            alt='logo'
          />
        </Link>
        {![HOME_ROUTE, LOGIN_ROUTE, USER_ROUTE].includes(currentRouteName) && (
          <ul className={s.menu}>
            {MENU.map(item =>
              <li
                key={item.label}
                className={cn(s.itemWrapper, currentRouteName === item.routeName && s.active)}
              >
                <Link to={item.routeName} className={s.item}>
                  {React.createElement(item.iconComponent, {
                    className: s.icon
                  })}
                  {item.label}
                </Link>
              </li>
            )}
          </ul>
        )}
      </nav>
    )
  }
}

const mapState = state => ({
  sidebarOpened: state.global.sidebarOpened,
  currentRouteName: state.global.currentRouteName,
})

const mapDispatch = {}

export default connect(mapState, mapDispatch)(withStyles(s)(Sidebar))
