import React from 'react'
import {connect} from 'react-redux'
import {createForm} from 'rc-form'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './BcCustomAnalytics.css'
import {getCustomAnalytics} from '../../reducers/breastCancer'
import Tab from 'react-bootstrap/lib/Tab'
import Tabs from 'react-bootstrap/lib/Tabs'
import BcGeneralForm from './BcGeneralForm'
import BcSurvivalMonthsForm from './BcSurvivalMonthsForm'

class BcCustomAnalytics extends React.Component {
  render() {
    return (
      <Tabs
        id='contentTabs'
        justified
        animation={false}
        className={s.contentTabSection}
      >
        <Tab eventKey={0} title='General' className={s.tabContent}>
          <BcGeneralForm/>
        </Tab>
        <Tab eventKey={1} title='Survival months' className={s.tabContent}>
          <BcSurvivalMonthsForm/>
        </Tab>
      </Tabs>
    )
  }
}

const mapState = state => ({
  ...state.breastCancer,
})

const mapDispatch = {
  getCustomAnalytics,
}

export default connect(mapState, mapDispatch)(createForm()(withStyles(s)(BcCustomAnalytics)))
