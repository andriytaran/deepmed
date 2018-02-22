import React from 'react'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './Dropdown.css'
import {Link} from '../../components'
import cn from 'classnames'
import BsDropdown from 'react-bootstrap/lib/Dropdown'
import RootCloseWrapper from 'react-overlays/lib/RootCloseWrapper'

// TODO make it better
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
        {to ? (
          <Link
            to={to}
            role='menuitem'
            tabIndex='-1'
            onClick={this.handleClick}
          >
            {children}
          </Link>
        ) : (
          <a
            role='menuitem'
            tabIndex='-1'
            onClick={this.handleClick}
          >
            {children}
          </a>
        )}
      </li>
    )
  }
}

class Dropdown extends React.Component {
  render() {
    return (
      <BsDropdown {...this.props}/>
    )
  }
}

Dropdown.Toggle = CustomToggle
Dropdown.Menu = CustomMenu
Dropdown.Item = MenuItem

export default withStyles(s)(Dropdown)
