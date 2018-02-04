import React from 'react'
import cn from 'classnames'

class Select extends React.Component {
  render() {
    const {label, error, children, ...otherProps} = this.props
    return (
      <div className={cn(error && 'has-error')}>
        {label && <label className='control-label'>{label}</label>}
        <select className="form-control" {...otherProps}>
          {children}
        </select>
        {error && <span className='help-block'>{error}</span>}
      </div>
    )
  }
}

export default Select
