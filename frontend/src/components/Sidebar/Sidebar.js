import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './Sidebar.css'
import {Link} from '../../components'
import {
  BC_CUSTOM_ANALYTICS_ROUTE,
  BC_DIAGNOSIS_ROUTE,
  BC_SURVIVAL_MONTHS,
  BC_FORM_ROUTE,
  BC_INDIVIDUAL_STATISTICS_ROUTE,
  BC_GLOBAL_STATISTICS_ROUTE,
  BC_US_STATISTICS_ROUTE,
  BC_RESOURCES_ROUTE,
  BC_SIMILAR_DIAGNOSES_ROUTE,
  BC_VISUALIZATION_ROUTE,
  HOME_ROUTE,
} from '../../routes'
import cn from 'classnames'
import FaHeaderO from 'react-icons/lib/fa/heart-o'
import FaBarChart from 'react-icons/lib/fa/bar-chart'
import FaFileO from 'react-icons/lib/fa/file-o'
import FaLaptop from 'react-icons/lib/fa/laptop'

const menuByModule = {
  bc: {
    baseRouteName: BC_FORM_ROUTE,
    items: [
      {routeName: BC_DIAGNOSIS_ROUTE, label: 'Diagnosis', iconComponent: FaHeaderO},
      {routeName: BC_VISUALIZATION_ROUTE, label: 'Visualization', iconComponent: FaHeaderO},
      {routeName: BC_GLOBAL_STATISTICS_ROUTE, label: 'Global Statistics', iconComponent: FaBarChart},
      {routeName: BC_US_STATISTICS_ROUTE, label: 'U.S. Statistics', iconComponent: FaBarChart},
      {routeName: BC_INDIVIDUAL_STATISTICS_ROUTE, label: 'Individual Statistics', iconComponent: FaBarChart},
      {routeName: BC_CUSTOM_ANALYTICS_ROUTE, label: 'Custom Analytics', iconComponent: FaBarChart},
      {routeName: BC_SURVIVAL_MONTHS, label: 'Survival Months', iconComponent: FaBarChart},
      {routeName: BC_SIMILAR_DIAGNOSES_ROUTE, label: 'Similar Diagnoses', iconComponent: FaFileO},
      {routeName: BC_RESOURCES_ROUTE, label: 'Resources', iconComponent: FaLaptop},
    ]
  },
}

class Sidebar extends React.Component {
  render() {
    const {sidebarOpened, currentRouteName, currentModule} = this.props
    const menu = menuByModule[currentModule]
    return (
      <nav className={cn(s.sidebar, sidebarOpened && s.opened)}>
        <Link to={menu ? menu.baseRouteName : HOME_ROUTE} className={s.logoWrapper}>
          <img
            className={s.logo}
            src={require('../../static/deep-med-logo-new.png')}
            alt='logo'
          />
        </Link>
        {menu && ![BC_FORM_ROUTE].includes(currentRouteName) && (
          <ul className={s.menu}>
            {menu.items.map(item =>
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
  currentModule: state.global.currentModule,
})

const mapDispatch = {}

export default connect(mapState, mapDispatch)(withStyles(s)(Sidebar))
