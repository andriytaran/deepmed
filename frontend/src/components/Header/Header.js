import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './Header.css'
import {Link, Row, Col} from '../../components'
import {LOGOUT_ROUTE, USER_ROUTE,} from '../../routes'
import cn from 'classnames'
import {Dropdown} from 'react-bootstrap'
import RootCloseWrapper from 'react-overlays/lib/RootCloseWrapper'
import {toggleSidebarOpened} from '../../reducers/global'

//TODO change bootstrap dropdown
class CustomToggle extends React.Component {
  handleClick = (e) => {
    e.preventDefault()

    this.props.onClick(e)
  }

  render() {
    return (
      <a
        className='dropdown-toggle user-dropdown inline-block'
        id='userDropdownMenu'
        onClick={this.handleClick}
      >
        {this.props.children}
      </a>
    )
  }
}

class CustomMenu extends React.Component {
  handleRootClose = (event) => {
    this.props.onClose(event, {source: 'rootClose'})
  }

  render() {
    const {children, open, onSelect} = this.props
    return (
      <RootCloseWrapper
        disabled={!open}
        onRootClose={this.handleRootClose}
        event={'click'}
      >
        <ul className='dropdown-menu dropdown-menu-right dropdown-menu-keep-open'>
          {React.Children.map(children, child => (
            React.cloneElement(child, {
              onSelect,
            })
          ))}
        </ul>
      </RootCloseWrapper>
    )
  }
}

class MenuItem extends React.Component {
  static defaultProps = {
    divider: false,
    disabled: false,
    header: false,
  }

  handleClick = (event) => {
    const {disabled, onSelect, eventKey} = this.props

    if (disabled) {
      event.preventDefault()
    }

    if (disabled) {
      return
    }

    if (onSelect) {
      onSelect(eventKey, event)
    }
  }

  render() {
    const {
      active,
      disabled,
      divider,
      header,
      onClick,
      className,
      style,
      children,
      to,
      ...props
    } = this.props
    return (
      <li
        role='presentation'
        className={cn(className, {active, disabled})}
        style={style}
      >
        <Link
          to={to}
          role='menuitem'
          tabIndex='-1'
          onClick={this.handleClick}
        >
          {children}
        </Link>
      </li>
    )
  }
}

class Header extends React.Component {
  render() {
    const {sidebarOpened, toggleSidebarOpened, title, loggedIn} = this.props
    return (
      <Row type='flex' justify='space-between' align='middle' className={s.header}>
        <a className={s.toggler} onClick={toggleSidebarOpened}>
          <i className={cn(s.togglerIcon, sidebarOpened ? 'fa fa-times' : 'fa fa-bars')}/>
        </a>

        <Col>
          <img src={require('../../static/icon-logo.png')} className={s.smallLogo}/>
          <h1 className={s.title}>{title}</h1>
        </Col>

        <Col>
          {loggedIn && (
            <Dropdown
              bsStyle='default'
              id='user'
            >
              <CustomToggle bsRole='toggle'>
                <img
                  className='arrow'
                  src={require('../../static/caret-down.png')}
                  width='10'
                  height='auto'
                />
              </CustomToggle>
              <CustomMenu bsRole='menu' rootCloseEvent={'click'}>
                <MenuItem to={USER_ROUTE}>Account</MenuItem>
                <MenuItem to={LOGOUT_ROUTE}>Log Out</MenuItem>
              </CustomMenu>
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
