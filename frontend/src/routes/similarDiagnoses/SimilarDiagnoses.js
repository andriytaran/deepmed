import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './SimilarDiagnoses.scss'

class SimilarDiagnoses extends React.Component {
  render() {
    const {data} = this.props
    return (
      <div className="container container-full" data-children="same-height">
        <div className="row">
          <div className="col-md-12">
            <div className="custom-panel custom-panel-condensed push-bot-0">
              <div className="scroll-y scroll-x max-height-700">
                <table className="table table-responsive table-middle-cell-align table-hover">
                  <thead>
                  <tr>
                    <th colSpan="4">
                      <h5 className="text-center">Diagnosis</h5>
                    </th>
                    <th colSpan="3">
                      <h5 className="text-center">Status</h5>
                    </th>
                    <th colSpan="5">
                    </th>
                    <th colSpan="3">
                      <h5 className="text-center">Treatment</h5>
                    </th>
                    <th colSpan="3">
                      <h5 className="text-center">Outcome</h5>
                    </th>
                  </tr>
                  <tr>
                    <th><h6 className="push-top-1">Age</h6></th>
                    <th><h6 className="push-top-1">Ethnicity</h6></th>
                    <th><h6 className="push-top-1">Size</h6></th>
                    <th><h6 className="push-top-1">Grade</h6></th>
                    <th><h6 className="push-top-1">ER</h6></th>
                    <th><h6 className="push-top-1">PR</h6></th>
                    <th><h6 className="push-top-1">HER2</h6></th>
                    <th><h6 className="push-top-1">Lat</h6></th>
                    <th><h6 className="push-top-1">Site</h6></th>
                    <th><h6 className="push-top-1">Type</h6></th>
                    <th><h6 className="push-top-1">Stage</h6></th>
                    <th><h6 className="push-top-1">+Nodes</h6></th>

                    <th><h6 className="push-top-1">Surgery</h6></th>
                    <th><h6 className="push-top-1">Chemo</h6></th>
                    <th><h6 className="push-top-1">Radiation</h6></th>
                    <th><h6 className="push-top-1">Year Dx</h6></th>
                    <th><h6 className="push-top-1">Survival Mos.</h6></th>
                    <th><h6 className="push-top-1">CoD</h6></th>
                  </tr>
                  </thead>
                  <tbody>
                  {data.similar_diagnosis.map((item, i) =>
                    <tr key={i}>
                      <td><p className="no-margin">{item['age-recode-with-single-ages-and-85']}</p></td>
                      <td><p className="no-margin">{item['race-ethnicity']}</p></td>
                      <td><p className="no-margin">{item['cs-tumor-size-2004']}</p></td>
                      <td><p className="no-margin">{item['grade']}</p></td>
                      <td><p className="no-margin">{item['er-status-recode-breast-cancer-1990']}</p></td>
                      <td><p className="no-margin">{item['pr-status-recode-breast-cancer-1990']}</p></td>
                      <td><p className="no-margin">{item['derived-her2-recode-2010-1']}</p></td>
                      <td><p className="no-margin">{item['laterality']}</p></td>
                      <td><p className="no-margin">{item['site-recode-icd-o-3-who-2008']}</p></td>
                      <td><p className="no-margin">{item['type']}</p></td>
                      <td><p className="no-margin">{item['2010-stage']}</p></td>
                      <td><p className="no-margin">{item['regional-nodes-positive-1988-1']}</p></td>
                      <td><p className="no-margin">{item['surgery']}</p></td>
                      <td><p className="no-margin">{item['chemo']}</p></td>
                      <td><p className="no-margin">{item['radiation-recode']}</p></td>
                      <td><p className="no-margin">{item['year-of-diagnosis']}</p></td>
                      <td><p className="no-margin">{item['survival-months']}</p></td>
                      <td><p className="no-margin">{item['cod-to-site-recode']}</p></td>
                    </tr>
                  )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

const mapState = state => ({
  ...state.diagnosis,
})

const mapDispatch = {}

export default connect(mapState, mapDispatch)(withStyles(s)(SimilarDiagnoses))
