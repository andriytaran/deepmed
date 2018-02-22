import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './Header.css'
import {Col, Dropdown, Row} from '../../components'
import {LOGOUT_ROUTE, USER_ROUTE, BC_FORM_ROUTE} from '../../routes'
import {toggleSidebarOpened} from '../../reducers/global'
import FaClose from 'react-icons/lib/fa/close'
import FaBars from 'react-icons/lib/fa/bars'

// TODO dropdowns
class Header extends React.Component {
  render() {
    const {sidebarOpened, toggleSidebarOpened, title, loggedIn} = this.props
    return (
      <Row type='flex' justify='space-between' align='middle' className={s.header}>
        <a className={s.toggler} onClick={toggleSidebarOpened}>
          {sidebarOpened ? (
            <FaClose className={s.togglerIcon}/>
          ) : (
            <FaBars className={s.togglerIcon}/>
          )}
        </a>

        <Col>
          <img src={require('../../static/icon-logo.png')} className={s.smallLogo}/>
          <h1 className={s.title}>{title}</h1>
        </Col>

        <Col>
          {/*<Dropdown*/}
            {/*className={s.dropdown}*/}
            {/*bsStyle='default'*/}
            {/*id='oncology'*/}
          {/*>*/}
            {/*<Dropdown.Toggle bsRole='toggle'>*/}
              {/*<span className={s.dropdownLabel}>DeepMed Oncology</span>*/}
              {/*<img*/}
                {/*className='arrow'*/}
                {/*src={require('../../static/caret-down.png')}*/}
                {/*width='10'*/}
                {/*height='auto'*/}
              {/*/>*/}
            {/*</Dropdown.Toggle>*/}
            {/*<Dropdown.Menu bsRole='menu'>*/}
              {/*<Dropdown.Item to={BC_FORM_ROUTE}>Breast Cancer</Dropdown.Item>*/}
              {/*<Dropdown.Item>Prostate Cancer</Dropdown.Item>*/}
            {/*</Dropdown.Menu>*/}
          {/*</Dropdown>*/}
          {/*<Dropdown*/}
            {/*className={s.dropdown}*/}
            {/*bsStyle='default'*/}
            {/*id='oncology'*/}
          {/*>*/}
            {/*<Dropdown.Toggle bsRole='toggle'>*/}
              {/*<span className={s.dropdownLabel}>DeepMed Pediatrics</span>*/}
              {/*<img*/}
                {/*className='arrow'*/}
                {/*src={require('../../static/caret-down.png')}*/}
                {/*width='10'*/}
                {/*height='auto'*/}
              {/*/>*/}
            {/*</Dropdown.Toggle>*/}
            {/*<Dropdown.Menu bsRole='menu'>*/}
              {/*<Dropdown.Item>...</Dropdown.Item>*/}
              {/*<Dropdown.Item>...</Dropdown.Item>*/}
            {/*</Dropdown.Menu>*/}
          {/*</Dropdown>*/}
          {loggedIn && (
            <Dropdown
              bsStyle='default'
              id='user'
            >
              <Dropdown.Toggle bsRole='toggle'>
                <img
                  className='arrow'
                  src={require('../../static/caret-down.png')}
                  width='10'
                  height='auto'
                />
              </Dropdown.Toggle>
              <Dropdown.Menu bsRole='menu'>
                <Dropdown.Item to={USER_ROUTE}>Account</Dropdown.Item>
                <Dropdown.Item to={LOGOUT_ROUTE}>Log Out</Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
          )}
        </Col>
      </Row>
    )
  }
}

const mapState = state => ({
  sidebarOpened: state.global.sidebarOpened,
  loggedIn: state.user.loggedIn,
})

const mapDispatch = {
  toggleSidebarOpened,
}

export default connect(mapState, mapDispatch)(withStyles(s)(Header))
