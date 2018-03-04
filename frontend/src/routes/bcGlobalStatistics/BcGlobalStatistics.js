import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './BcGlobalStatistics.css'
import {Col, Row, VectorMap} from '../../components'
import {HorizontalBar} from 'react-chartjs-2'
import reduce from 'lodash/reduce'
import assign from 'lodash/assign'
import uniq from 'lodash/uniq'
import sortBy from 'lodash/sortBy'
import cn from 'classnames'

const white = '#fff'
const color_1 = 'rgba(0, 125, 255, 0.75)'
const color_3 = 'rgba(72, 204, 245, 0.75)'

const colors = ['#47cfd1', '#47cfd1', '#04a9a9', '#48ccf5', '#77c2d9', '#77c2d9']

const map_data = [
  {
    'name': 'Burundi',
    'value': 23.5,
    'code': 'BI',
    'range': '22+'
  },
  {
    'name': 'Comoros',
    'value': 17.4,
    'code': 'KM',
    'range': '10+'
  },
  {
    'name': 'Djibouti',
    'value': 35.9,
    'code': 'DJ',
    'range': '22+'
  },
  {
    'name': 'Eritrea',
    'value': 35.9,
    'code': 'ER',
    'range': '22+'
  },
  {
    'name': 'Ethiopia',
    'value': 41.8,
    'code': 'ET',
    'range': '40+'
  },
  {
    'name': 'France, La Reunion',
    'value': 46.6,
    'code': 'FR-RE',
    'range': '40+'
  },
  {
    'name': 'Kenya',
    'value': 38.3,
    'code': 'KE',
    'range': '22+'
  },
  {
    'name': 'Madagascar',
    'value': 26.6,
    'code': 'MG',
    'range': '22+'
  },
  {
    'name': 'Malawi',
    'value': 16.8,
    'code': 'MW',
    'range': '10+'
  },
  {
    'name': 'Mauritius',
    'value': 64.2,
    'code': 'MU',
    'range': '57+'
  },
  {
    'name': 'Mozambique',
    'value': 14.5,
    'code': 'MZ',
    'range': '10+'
  },
  {
    'name': 'Rwanda',
    'value': 15.9,
    'code': 'RW',
    'range': '10+'
  },
  {
    'name': 'Somalia',
    'value': 40.6,
    'code': 'SO',
    'range': '40+'
  },
  {
    'name': 'South Sudan',
    'value': 31.8,
    'code': 'SS',
    'range': '22+'
  },
  {
    'name': 'Tanzania',
    'value': 19.4,
    'code': 'TZ',
    'range': '10+'
  },
  {
    'name': 'Uganda',
    'value': 27.5,
    'code': 'UG',
    'range': '22+'
  },
  {
    'name': 'Zambia',
    'value': 22.4,
    'code': 'ZM',
    'range': '22+'
  },
  {
    'name': 'Zimbabwe',
    'value': 28.5,
    'code': 'ZW',
    'range': '22+'
  },
  {
    'name': 'Angola',
    'value': 23.5,
    'code': 'AO',
    'range': '22+'
  },
  {
    'name': 'Cameroon',
    'value': 35.2,
    'code': 'CM',
    'range': '22+'
  },
  {
    'name': 'Central African Republic',
    'value': 31.4,
    'code': 'CF',
    'range': '22+'
  },
  {
    'name': 'Chad',
    'value': 34.1,
    'code': 'TD',
    'range': '22+'
  },
  {
    'name': 'Democratic Republic of the Congo',
    'value': 23.5,
    'code': 'CD',
    'range': '22+'
  },
  {
    'name': 'Congo',
    'value': 31.7,
    'code': 'CG',
    'range': '22+'
  },
  {
    'name': 'Equatorial Guinea',
    'value': 25.2,
    'code': 'GQ',
    'range': '22+'
  },
  {
    'name': 'Gabon',
    'value': 16.1,
    'code': 'GA',
    'range': '10+'
  },
  {
    'name': 'Algeria',
    'value': 48.5,
    'code': 'DZ',
    'range': '40+'
  },
  {
    'name': 'Egypt',
    'value': 49.5,
    'code': 'EG',
    'range': '40+'
  },
  {
    'name': 'Libya',
    'value': 24.1,
    'code': 'LY',
    'range': '22+'
  },
  {
    'name': 'Morocco',
    'value': 40.8,
    'code': 'MA',
    'range': '40+'
  },
  {
    'name': 'Sudan',
    'value': 27.8,
    'code': 'SD',
    'range': '22+'
  },
  {
    'name': 'Tunisia',
    'value': 31.8,
    'code': 'TN',
    'range': '22+'
  },
  {
    'name': 'Western Sahara',
    'value': 36.2,
    'code': 'EH',
    'range': '22+'
  },
  {
    'name': 'Botswana',
    'value': 19.9,
    'code': 'BW',
    'range': '10+'
  },
  {
    'name': 'Lesotho',
    'value': 9.0,
    'code': 'LS',
    'range': '10+'
  },
  {
    'name': 'Namibia',
    'value': 24.4,
    'code': 'NA',
    'range': '22+'
  },
  {
    'name': 'South Africa',
    'value': 41.5,
    'code': 'ZA',
    'range': '40+'
  },
  {
    'name': 'Swaziland',
    'value': 10.5,
    'code': 'SZ',
    'range': '10+'
  },
  {
    'name': 'Benin',
    'value': 30.2,
    'code': 'BJ',
    'range': '22+'
  },
  {
    'name': 'Burkina Faso',
    'value': 22.7,
    'code': 'BF',
    'range': '22+'
  },
  {
    'name': 'Cap Verde',
    'value': 25.1,
    'code': 'CV',
    'range': '22+'
  },
  {
    'name': 'Cote d Ivoire',
    'value': 33.7,
    'code': 'CI',
    'range': '22+'
  },
  {
    'name': 'The Gambia',
    'value': 9.8,
    'code': 'GM',
    'range': '10+'
  },
  {
    'name': 'Ghana',
    'value': 25.6,
    'code': 'GH',
    'range': '22+'
  },
  {
    'name': 'Guinea',
    'value': 14.5,
    'code': 'GN',
    'range': '10+'
  },
  {
    'name': 'Guinea-Bissau',
    'value': 26.0,
    'code': 'GW',
    'range': '22+'
  },
  {
    'name': 'Liberia',
    'value': 24.1,
    'code': 'LR',
    'range': '22+'
  },
  {
    'name': 'Mali',
    'value': 29.8,
    'code': 'ML',
    'range': '22+'
  },
  {
    'name': 'Mauritania',
    'value': 25.8,
    'code': 'MR',
    'range': '22+'
  },
  {
    'name': 'Niger',
    'value': 23.8,
    'code': 'NE',
    'range': '22+'
  },
  {
    'name': 'Nigeria',
    'value': 50.4,
    'code': 'NG',
    'range': '40+'
  },
  {
    'name': 'Senegal',
    'value': 22.4,
    'code': 'SN',
    'range': '22+'
  },
  {
    'name': 'Sierra Leone',
    'value': 24.3,
    'code': 'SL',
    'range': '22+'
  },
  {
    'name': 'Togo',
    'value': 27.2,
    'code': 'TG',
    'range': '22+'
  },
  {
    'name': 'Bahamas',
    'value': 98.9,
    'code': 'BS',
    'range': '92+'
  },
  {
    'name': 'Barbados',
    'value': 94.7,
    'code': 'BB',
    'range': '92+'
  },
  {
    'name': 'Cuba',
    'value': 50.4,
    'code': 'CU',
    'range': '40+'
  },
  {
    'name': 'Dominican Republic',
    'value': 38.1,
    'code': 'DO',
    'range': '22+'
  },
  {
    'name': 'France, Guadeloupe',
    'value': 53.7,
    'code': 'FR-GP',
    'range': '40+'
  },
  {
    'name': 'France, Martinique',
    'value': 59.6,
    'code': 'FR-MQ',
    'range': '57+'
  },
  {
    'name': 'Haiti',
    'value': 22.0,
    'code': 'HT',
    'range': '22+'
  },
  {
    'name': 'Jamaica',
    'value': 55.8,
    'code': 'JM',
    'range': '40+'
  },
  {
    'name': 'Puerto Rico',
    'value': 57.5,
    'code': 'PR',
    'range': '57+'
  },
  {
    'name': 'Trinidad and Tobago',
    'value': 56.9,
    'code': 'TT',
    'range': '40+'
  },
  {
    'name': 'Belize',
    'value': 39.6,
    'code': 'BZ',
    'range': '22+'
  },
  {
    'name': 'Costa Rica',
    'value': 45.4,
    'code': 'CR',
    'range': '40+'
  },
  {
    'name': 'El Salvador',
    'value': 23.7,
    'code': 'SV',
    'range': '22+'
  },
  {
    'name': 'Guatemala',
    'value': 11.9,
    'code': 'GT',
    'range': '10+'
  },
  {
    'name': 'Honduras',
    'value': 19.9,
    'code': 'HN',
    'range': '10+'
  },
  {
    'name': 'Mexico',
    'value': 35.4,
    'code': 'MX',
    'range': '22+'
  },
  {
    'name': 'Nicaragua',
    'value': 23.9,
    'code': 'NI',
    'range': '22+'
  },
  {
    'name': 'Panama',
    'value': 43.0,
    'code': 'PA',
    'range': '40+'
  },
  {
    'name': 'Argentina',
    'value': 71.2,
    'code': 'AR',
    'range': '57+'
  },
  {
    'name': 'Bolivia',
    'value': 19.2,
    'code': 'BO',
    'range': '10+'
  },
  {
    'name': 'Brazil',
    'value': 59.5,
    'code': 'BR',
    'range': '57+'
  },
  {
    'name': 'Chile',
    'value': 34.8,
    'code': 'CL',
    'range': '22+'
  },
  {
    'name': 'Colombia',
    'value': 35.7,
    'code': 'CO',
    'range': '22+'
  },
  {
    'name': 'Ecuador',
    'value': 32.7,
    'code': 'EC',
    'range': '22+'
  },
  {
    'name': 'French Guiana',
    'value': 37.1,
    'code': 'GF',
    'range': '22+'
  },
  {
    'name': 'Guyana',
    'value': 50.4,
    'code': 'GY',
    'range': '40+'
  },
  {
    'name': 'Paraguay',
    'value': 43.8,
    'code': 'PY',
    'range': '40+'
  },
  {
    'name': 'Peru',
    'value': 28.0,
    'code': 'PE',
    'range': '22+'
  },
  {
    'name': 'Suriname',
    'value': 41.4,
    'code': 'SR',
    'range': '40+'
  },
  {
    'name': 'Uruguay',
    'value': 69.8,
    'code': 'UY',
    'range': '57+'
  },
  {
    'name': 'Venezuela',
    'value': 41.2,
    'code': 'VE',
    'range': '40+'
  },
  {
    'name': 'Canada',
    'value': 79.8,
    'code': 'CA',
    'range': '74+'
  },
  {
    'name': 'United States of America',
    'value': 92.9,
    'code': 'US',
    'range': '92+'
  },
  {
    'name': 'China',
    'value': 22.1,
    'code': 'CN',
    'range': '22+'
  },
  {
    'name': 'Japan',
    'value': 51.5,
    'code': 'JP',
    'range': '40+'
  },
  {
    'name': 'North Korea',
    'value': 36.8,
    'code': 'KP',
    'range': '22+'
  },
  {
    'name': 'Korea',
    'value': 52.1,
    'code': 'KR',
    'range': '40+'
  },
  {
    'name': 'Mongolia',
    'value': 9.4,
    'code': 'MN',
    'range': '10+'
  },
  {
    'name': 'Brunei',
    'value': 48.6,
    'code': 'BN',
    'range': '40+'
  },
  {
    'name': 'Cambodia',
    'value': 19.3,
    'code': 'KH',
    'range': '10+'
  },
  {
    'name': 'Indonesia',
    'value': 40.3,
    'code': 'ID',
    'range': '40+'
  },
  {
    'name': 'Lao PDR',
    'value': 19.0,
    'code': 'LA',
    'range': '10+'
  },
  {
    'name': 'Malaysia',
    'value': 38.7,
    'code': 'MY',
    'range': '22+'
  },
  {
    'name': 'Myanmar',
    'value': 22.1,
    'code': 'MM',
    'range': '22+'
  },
  {
    'name': 'Philippines',
    'value': 47.0,
    'code': 'PH',
    'range': '40+'
  },
  {
    'name': 'Singapore',
    'value': 65.7,
    'code': 'SG',
    'range': '57+'
  },
  {
    'name': 'Thailand',
    'value': 29.3,
    'code': 'TH',
    'range': '22+'
  },
  {
    'name': 'Timor-Leste',
    'value': 32.6,
    'code': 'TL',
    'range': '22+'
  },
  {
    'name': 'Viet Nam',
    'value': 23.0,
    'code': 'VN',
    'range': '22+'
  },
  {
    'name': 'Afghanistan',
    'value': 35.1,
    'code': 'AF',
    'range': '22+'
  },
  {
    'name': 'Bangladesh',
    'value': 21.7,
    'code': 'BD',
    'range': '10+'
  },
  {
    'name': 'Bhutan',
    'value': 4.6,
    'code': 'BT',
    'range': '10+'
  },
  {
    'name': 'India',
    'value': 25.8,
    'code': 'IN',
    'range': '22+'
  },
  {
    'name': 'Iran',
    'value': 28.1,
    'code': 'IR',
    'range': '22+'
  },
  {
    'name': 'Kazakhstan',
    'value': 63.0,
    'code': 'KZ',
    'range': '57+'
  },
  {
    'name': 'Kyrgyzstan',
    'value': 27.3,
    'code': 'KG',
    'range': '22+'
  },
  {
    'name': 'Maldives',
    'value': 31.6,
    'code': 'MV',
    'range': '22+'
  },
  {
    'name': 'Nepal',
    'value': 13.7,
    'code': 'NP',
    'range': '10+'
  },
  {
    'name': 'Pakistan',
    'value': 50.3,
    'code': 'PK',
    'range': '40+'
  },
  {
    'name': 'Sri Lanka',
    'value': 30.9,
    'code': 'LK',
    'range': '22+'
  },
  {
    'name': 'Tajikistan',
    'value': 20.4,
    'code': 'TJ',
    'range': '10+'
  },
  {
    'name': 'Turkmenistan',
    'value': 26.8,
    'code': 'TM',
    'range': '22+'
  },
  {
    'name': 'Uzbekistan',
    'value': 27.1,
    'code': 'UZ',
    'range': '22+'
  },
  {
    'name': 'Armenia',
    'value': 74.1,
    'code': 'AM',
    'range': '74+'
  },
  {
    'name': 'Azerbaijan',
    'value': 25.4,
    'code': 'AZ',
    'range': '22+'
  },
  {
    'name': 'Bahrain',
    'value': 42.5,
    'code': 'BH',
    'range': '40+'
  },
  {
    'name': 'State of Palestine',
    'value': 44.0,
    'code': 'PS',
    'range': '40+'
  },
  {
    'name': 'Georgia',
    'value': 44.0,
    'code': 'GE',
    'range': '40+'
  },
  {
    'name': 'Iraq',
    'value': 42.6,
    'code': 'IQ',
    'range': '40+'
  },
  {
    'name': 'Israel',
    'value': 80.5,
    'code': 'IL',
    'range': '74+'
  },
  {
    'name': 'Jordan',
    'value': 61.0,
    'code': 'JO',
    'range': '57+'
  },
  {
    'name': 'Kuwait',
    'value': 46.7,
    'code': 'KW',
    'range': '40+'
  },
  {
    'name': 'Lebanon',
    'value': 78.7,
    'code': 'LB',
    'range': '74+'
  },
  {
    'name': 'Oman',
    'value': 26.0,
    'code': 'OM',
    'range': '22+'
  },
  {
    'name': 'Qatar',
    'value': 46.1,
    'code': 'QA',
    'range': '40+'
  },
  {
    'name': 'Saudi Arabia',
    'value': 29.5,
    'code': 'SA',
    'range': '22+'
  },
  {
    'name': 'Syrian Arab Republic',
    'value': 52.5,
    'code': 'SY',
    'range': '40+'
  },
  {
    'name': 'Turkey',
    'value': 39.1,
    'code': 'TR',
    'range': '22+'
  },
  {
    'name': 'United Arab Emirates',
    'value': 39.2,
    'code': 'AE',
    'range': '22+'
  },
  {
    'name': 'Yemen',
    'value': 27.4,
    'code': 'YE',
    'range': '22+'
  },
  {
    'name': 'Belarus',
    'value': 45.9,
    'code': 'BY',
    'range': '40+'
  },
  {
    'name': 'Bulgaria',
    'value': 58.5,
    'code': 'BG',
    'range': '57+'
  },
  {
    'name': 'Czech Republic',
    'value': 70.3,
    'code': 'CZ',
    'range': '57+'
  },
  {
    'name': 'Hungary',
    'value': 54.5,
    'code': 'HU',
    'range': '40+'
  },
  {
    'name': 'Republic of Moldova',
    'value': 38.7,
    'code': 'MD',
    'range': '22+'
  },
  {
    'name': 'Poland',
    'value': 51.9,
    'code': 'PL',
    'range': '40+'
  },
  {
    'name': 'Romania',
    'value': 50.0,
    'code': 'RO',
    'range': '40+'
  },
  {
    'name': 'Russian Federation',
    'value': 45.6,
    'code': 'RU',
    'range': '40+'
  },
  {
    'name': 'Slovakia',
    'value': 57.5,
    'code': 'SK',
    'range': '57+'
  },
  {
    'name': 'Ukraine',
    'value': 41.3,
    'code': 'UA',
    'range': '40+'
  },
  {
    'name': 'Denmark',
    'value': 105.0,
    'code': 'DK',
    'range': '92+'
  },
  {
    'name': 'Estonia',
    'value': 51.6,
    'code': 'EE',
    'range': '40+'
  },
  {
    'name': 'Finland',
    'value': 89.4,
    'code': 'FI',
    'range': '74+'
  },
  {
    'name': 'Iceland',
    'value': 96.3,
    'code': 'IS',
    'range': '92+'
  },
  {
    'name': 'Ireland',
    'value': 92.3,
    'code': 'IE',
    'range': '92+'
  },
  {
    'name': 'Latvia',
    'value': 52.1,
    'code': 'LV',
    'range': '40+'
  },
  {
    'name': 'Lithuania',
    'value': 48.7,
    'code': 'LT',
    'range': '40+'
  },
  {
    'name': 'Norway',
    'value': 73.1,
    'code': 'NO',
    'range': '57+'
  },
  {
    'name': 'Sweden',
    'value': 80.4,
    'code': 'SE',
    'range': '74+'
  },
  {
    'name': 'United Kingdom',
    'value': 95.0,
    'code': 'GB',
    'range': '92+'
  },
  {
    'name': 'Albania',
    'value': 53.9,
    'code': 'AL',
    'range': '40+'
  },
  {
    'name': 'Bosnia Herzegovina',
    'value': 37.4,
    'code': 'BA',
    'range': '22+'
  },
  {
    'name': 'Croatia',
    'value': 60.9,
    'code': 'HR',
    'range': '57+'
  },
  {
    'name': 'Cyprus',
    'value': 78.4,
    'code': 'CY',
    'range': '74+'
  },
  {
    'name': 'Greece',
    'value': 43.9,
    'code': 'GR',
    'range': '40+'
  },
  {
    'name': 'Italy',
    'value': 91.3,
    'code': 'IT',
    'range': '74+'
  },
  {
    'name': 'FYR Macedonia',
    'value': 76.2,
    'code': 'MK',
    'range': '74+'
  },
  {
    'name': 'Malta',
    'value': 85.9,
    'code': 'MT',
    'range': '74+'
  },
  {
    'name': 'Montenegro',
    'value': 59.7,
    'code': 'ME',
    'range': '57+'
  },
  {
    'name': 'Portugal',
    'value': 67.6,
    'code': 'PT',
    'range': '57+'
  },
  {
    'name': 'Serbia',
    'value': 69.0,
    'code': 'RS',
    'range': '57+'
  },
  {
    'name': 'Slovenia',
    'value': 66.5,
    'code': 'SI',
    'range': '57+'
  },
  {
    'name': 'Spain',
    'value': 67.3,
    'code': 'ES',
    'range': '57+'
  },
  {
    'name': 'Austria',
    'value': 68.0,
    'code': 'AT',
    'range': '57+'
  },
  {
    'name': 'Belgium',
    'value': 111.9,
    'code': 'BE',
    'range': '92+'
  },
  {
    'name': 'France',
    'value': 89.7,
    'code': 'FR',
    'range': '74+'
  },
  {
    'name': 'Germany',
    'value': 91.6,
    'code': 'DE',
    'range': '74+'
  },
  {
    'name': 'Luxembourg',
    'value': 89.1,
    'code': 'LU',
    'range': '74+'
  },
  {
    'name': 'The Netherlands',
    'value': 99.0,
    'code': 'NL',
    'range': '92+'
  },
  {
    'name': 'Switzerland',
    'value': 83.1,
    'code': 'CH',
    'range': '74+'
  },
  {
    'name': 'Australia',
    'value': 86.0,
    'code': 'AU',
    'range': '74+'
  },
  {
    'name': 'New Zealand',
    'value': 85.0,
    'code': 'NZ',
    'range': '74+'
  },
  {
    'name': 'Fiji',
    'value': 65.0,
    'code': 'FJ',
    'range': '57+'
  },
  {
    'name': 'New Caledonia',
    'value': 87.6,
    'code': 'NC',
    'range': '74+'
  },
  {
    'name': 'Papua New Guinea',
    'value': 33.7,
    'code': 'PG',
    'range': '22+'
  },
  {
    'name': 'Solomon Islands',
    'value': 47.6,
    'code': 'SB',
    'range': '40+'
  },
  {
    'name': 'Vanuatu',
    'value': 31.8,
    'code': 'VU',
    'range': '22+'
  },
  {
    'name': 'Guam',
    'value': 49.4,
    'code': 'GU',
    'range': '40+'
  },
  {
    'name': 'French Polynesia',
    'value': 92.2,
    'code': 'PF',
    'range': '92+'
  },
  {
    'name': 'Samoa',
    'value': 23.2,
    'code': 'WS',
    'range': '22+'
  }
]

const bar_chart_data = {
  labels: ['Northern America', 'Western Europe', 'Northern Europe', 'Australia/New Zealand', 'Oceania', 'Southern Europe', 'Europe', 'Polynesia', 'Micronesia/Polynesia', 'South America', 'Micronesia', 'Central and Eastern Europe', 'Latin America and Caribbean', 'Caribbean', 'Northern Africa', 'World', 'Western Asia', 'Melanesia', 'Southern Africa', 'Western Africa', 'Africa', 'South-Eastern Asia', 'Sub-Saharan Africa', 'Central America', 'Eastern Africa', 'Asia', 'South-Central Asia', 'Eastern Asia', 'Middle Africa'],
  datasets: [
    {
      label: 'Incidence',
      backgroundColor: color_1,
      hoverBackgroundColor: color_1,
      borderColor: white,
      data: [91.6, 91.1, 89.4, 85.8, 79.2, 74.5, 69.9, 68.9, 59.7, 52.1, 48.8, 47.7, 47.2, 46.1, 43.2, 43.1, 42.8, 41.0, 38.9, 38.6, 36.2, 34.8, 33.8, 32.8, 30.4, 29.1, 28.2, 27.0, 26.8],
    },
    {
      label: 'Mortality',
      backgroundColor: color_3,
      hoverBackgroundColor: color_3,
      borderColor: white,
      data: [14.8, 16.2, 16.4, 14.5, 15.6, 14.9, 16.1, 15.4, 13.1, 14.0, 10.4, 16.5, 13.0, 15.1, 17.4, 12.9, 15.1, 19.7, 15.5, 20.1, 17.3, 14.1, 17.2, 9.5, 15.6, 10.2, 13.5, 6.1, 14.8],
    }
  ]
}

class BcGlobalStatistics extends React.Component {
  render() {
    let countries
    let ranges
    if (map_data && map_data.length) {
      countries = reduce(map_data, (acc, {code, range}) => assign(acc, {[code]: range}), {})
      ranges = sortBy(uniq(map_data.map(item => item.range)), x => x)
    }

    return (
      <div className={s.container}>
        <Row type='flex' gutter={16}>
          <Col xs={24} md={16} className={s.col}>
            <div className={cn(s.card, s.mapCard)}>
              <h2 className={s.cardHeader}>Breast Cancer Incidence per 100,000</h2>
              <div className={s.mapWrapper}>
                <VectorMap
                  map='world_mill'
                  backgroundColor='transparent'
                  series={{
                    regions: [{
                      values: countries,
                      scale: {
                        '10+': '#47cfd1',
                        '22+': '#47cfd1',
                        '40+': '#04a9a9',
                        '57+': '#48ccf5',
                        '74+': '#77c2d9',
                        '92+': '#77c2d9',
                      }
                    }]
                  }}
                  containerStyle={{width: '100%', height: 500}}
                  onRegionTipShow={(e, el, code) => {
                    const currentCountry = map_data.find(item => code.includes(item.code)) || {}
                    el.html(el.html() + `<div>Range: ${currentCountry.range}<br/>Value: ${currentCountry.value}</div>`)
                  }}
                  regionStyle={{
                    initial: {
                      stroke: 'white',
                      'stroke-width': 2,
                      'stroke-opacity': 1,
                    },
                  }}
                />
              </div>
              {ranges && (
                <div className={s.rangesCard}>
                  <p className={s.rangesCardHeader}>Range:</p>
                  <Row type='flex' gutter={4} justify='space-between' align='middle' className={s.rangesCardContent}>
                      <Col  className={s.range}>
                        <span className={s.rangeIndicator} style={{backgroundColor: '#47cfd1'}}/>
                        <p className={s.rangeLabel}>10+</p>
                        <span className={s.rangeIndicator} style={{backgroundColor: '#04a9a9'}}/>
                        <p className={s.rangeLabel}>40+</p>
                        <span className={s.rangeIndicator} style={{backgroundColor: '#48ccf5'}}/>
                        <p className={s.rangeLabel}>57+</p>
                        <span className={s.rangeIndicator} style={{backgroundColor: '#77c2d9'}}/>
                        <p className={s.rangeLabel}>74+</p>
                      </Col>
                  </Row>
                </div>
              )}
            </div>
            <Row type='flex' gutter={16}>
              <Col xs={24} md={12} className={s.col}>
                <Row>
                  <div className={cn(s.card, s.fullHeight)}>
                    <div className={s.labels}>
                      <div className='row row-condensed'>
                        <div className='col-sm-6'>
                          <div className='custom-panel custom-panel-condensed no border green-bg push-bot-0'>
                            <div className='display-table display-table-100'>
                              <div className='display-table-cell'>
                                <p className='no-margin text-white small'>
                                  Estimated New<br/>Cases in 2017
                                </p>
                              </div>
                              <div className='display-table-cell text-right'>
                                <p className='no-margin text-white'>
                                  <strong>1.7m</strong>
                                </p>
                              </div>
                            </div>
                          </div>
                          <div className='custom-panel custom-panel-condensed no border green-bg push-bot-0'>
                            <div className='display-table display-table-100'>
                              <div className='display-table-cell'>
                                <p className='no-margin text-white small'>
                                  % of All New<br/>Cancer Cases
                                </p>
                              </div>
                              <div className='display-table-cell text-right'>
                                <p className='no-margin text-white'>
                                  <strong>25.2%</strong>
                                </p>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div className='col-sm-6'>
                          <div className='custom-panel custom-panel-condensed no border blue-bg push-bot-0'>
                            <div className='display-table display-table-100'>
                              <div className='display-table-cell'>
                                <p className='no-margin text-white small'>
                                  Estimated<br/>Deaths in 2017
                                </p>
                              </div>
                              <div className='display-table-cell text-right'>
                                <p className='no-margin text-white'>
                                  <strong>522,000</strong>
                                </p>
                              </div>
                            </div>
                          </div>
                          <div className='custom-panel custom-panel-condensed no border blue-bg push-bot-0'>
                            <div className='display-table display-table-100'>
                              <div className='display-table-cell'>
                                <p className='no-margin text-white small'>
                                  % of All<br/>Cancer Deaths
                                </p>
                              </div>
                              <div className='display-table-cell text-right'>
                                <p className='no-margin text-white'>
                                  <strong>15.0%</strong>
                                </p>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </Row>

              </Col>
              <Col xs={24} md={12} className={s.col}>
                <div className={s.card}>
                  <ul className={s.list}>
                    <li>
                      Breast cancer survival rates vary greatly worldwide, ranging from 80% or over in North America,
                      Sweden
                      and Japan to around 60% in middle-income countries and below 40% in low-income countries.
                    </li>
                    <li>
                      The low survival rates in less developed countries can be explained mainly by the lack of early
                      detection programs, resulting in a high proportion of women presenting with late-stage disease, as
                      well
                      as by the lack of adequate diagnosis and treatment facilities.
                    </li>
                  </ul>
                </div>
              </Col>
            </Row>
            <Row>
                <div className={s.card}>
                  <h2 className={s.cardHeader}>Five Year Survival Rate</h2>
                  <Row type='flex' gutter={16} className={s.row}>
                    <Col>
                      <div className='display-table-cell display-block-xs'>
                        <div
                          className='custom-panel custom-panel-condensed gradient-bg text-center push-bot-0'>
                          <p className='no-margin text-white'><strong>US</strong></p>
                          <p className='font-size-20 push-top-1 push-bot-1 text-white'>
                            <strong>89.7%</strong></p>
                        </div>
                      </div>
                    </Col>
                    <Col>
                      <div className='display-table-cell display-block-xs'>
                        <div
                          className='custom-panel custom-panel-condensed gradient-bg text-center push-bot-0'>
                          <p className='no-margin text-white'><strong>Australia</strong></p>
                          <p className='font-size-20 push-top-1 push-bot-1 text-white'>
                            <strong>89.5%</strong></p>
                        </div>
                      </div>
                    </Col>
                    <Col>
                      <div className='display-table-cell display-block-xs'>
                        <div
                          className='custom-panel custom-panel-condensed gradient-bg text-center push-bot-0'>
                          <p className='no-margin text-white'><strong>India</strong></p>
                          <p className='font-size-20 push-top-1 push-bot-1 text-white'>
                            <strong>66.1%</strong></p>
                        </div>
                      </div>
                    </Col>
                    <Col>
                      <div className='display-table-cell display-block-xs'>
                        <div
                          className='custom-panel custom-panel-condensed gradient-bg text-center push-bot-0'>
                          <p className='no-margin text-white'><strong>China</strong></p>
                          <p className='font-size-20 push-top-1 push-bot-1 text-white'>
                            <strong>83.7%</strong></p>
                        </div>
                      </div>
                    </Col>
                    <Col>
                      <div className='display-table-cell display-block-xs'>
                        <div
                          className='custom-panel custom-panel-condensed gradient-bg text-center push-bot-0'>
                          <p className='no-margin text-white'><strong>Japan</strong></p>
                          <p className='font-size-20 push-top-1 push-bot-1 text-white'>
                            <strong>89.4%</strong></p>
                        </div>
                      </div>
                    </Col>
                    <Col>
                      <div className='display-table-cell display-block-xs'>
                        <div
                          className='custom-panel custom-panel-condensed gradient-bg text-center push-bot-0'>
                          <p className='no-margin text-white'><strong>Germany</strong></p>
                          <p className='font-size-20 push-top-1 push-bot-1 text-white'>
                            <strong>86.0%</strong></p>
                        </div>
                      </div>
                    </Col>
                    <Col>
                      <div className='display-table-cell display-block-xs'>
                        <div
                          className='custom-panel custom-panel-condensed gradient-bg text-center push-bot-0'>
                          <p className='no-margin text-white'><strong>UK</strong></p>
                          <p className='font-size-20 push-top-1 push-bot-1 text-white'>
                            <strong>85.6%</strong></p>
                        </div>
                      </div>
                    </Col>
                  </Row>
                </div>
            </Row>
          </Col>
          <Col xs={24} md={8} className={s.col}>
            <div className={cn(s.card, s.fullHeight)}>
              <h2 className={s.cardHeader}>Breast Cancer Incidence and Mortality per 100 000</h2>
              <HorizontalBar
                data={{
                  labels: bar_chart_data.labels,
                  datasets: bar_chart_data.datasets.map(item => ({
                    ...item,
                  }))
                }}
                options={{
                  legend: {
                    position: 'bottom',
                    display: true,
                  },
                  scales: {
                    xAxes: [{
                      ticks: {
                        beginAtZero: true,
                        stepSize: 20,
                      }
                    }]
                  },
                }}
                height={600}
                ref='chart'
              />
            </div>
          </Col>
        </Row>
      </div>
    )
  }
}

const mapState = state => ({
  ...state.breastCancer,
})

const mapDispatch = {}

export default connect(mapState, mapDispatch)(withStyles(s)(BcGlobalStatistics))
