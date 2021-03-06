export const WEEK = 604800
export const YEAR = 31536000

export const RACES = ['African American', 'American Indian/Alaska Native', 'Asian', 'Caucasian', 'Other']
export const RACES_FOR_PROSTATE = ['African American', 'American Indian/Alaska Native', 'Asian', 'Caucasian', 'Hispanics', 'Other'];

export const GROUPED_RACES = [
  'African American',
  'American Indian',
  {
    label: 'Asian',
    values: [
      'All Asian',
      'Chinese',
      'Japanese',
      'Korean',
      'Pacific Islander',
      'South Asian',
      'Thai',
      'Vietnamese'
    ]
  },
  'Caucasian',
  'Other',
]
export const GROUPED_SURVIVAL_MONTHS = [
  {value: 'chemo', label: 'Chemotherapy'},
  {value: 'radiation', label: 'Radiation'},
  {
    label: 'Surgery',
    values: [
      'Bi-Lateral Mastectomy',
      'Lumpectomy',
      'Mastectomy',
    ]
  }
]

export const AGES = [
  {value: 25, label: '20-30'},
  {value: 35, label: '30-40'},
  {value: 45, label: '40-50'},
  {value: 55, label: '50-60'},
  {value: 65, label: '60-70'},
  {value: 75, label: '70-80'},
  {value: 81, label: '80+'},
]

export const TUMOR_SIZES = [
  {value: '0-2cm', label: '0-2cm'},
  {value: '2-5cm', label: '2-5cm'},
  {value: '5cm+', label: '5cm+'},
]
export const TUMOR_GRADES = [
  {value: 1.0, label: '1 (Low)'},
  {value: 2.0, label: '2 (Medium)'},
  {value: 3.0, label: '3 (High)'},
  {value: 4.0, label: '4 (Very High)'},
]

export const NUMBER_OF_TUMORS = [
  {value: '1', label: '1'},
  {value: '2', label: '2'},
  {value: '3+', label: '3+'},
]

export const NUMBER_OF_NODES = [
  {value: '0', label: '0'},
  {value: '1-3', label: '1-3'},
  {value: '4-8', label: '4-8'},
  {value: '9+', label: '9+'},
]

export const SITES = [
  {value: 'Axillary', label: 'Axillary'},
  {value: 'Center', label: 'Center'},
  {value: 'Lower-Inner', label: 'Lower-Inner'},
  {value: 'Lower-Outer', label: 'Lower-Outer'},
  {value: 'Nipple', label: 'Nipple'},
  {value: 'NoS', label: 'NoS'},
  {value: 'Overlapping', label: 'Overlapping'},
  {value: 'Upper-Inner', label: 'Upper-Inner'},
  {value: 'Upper-Outer', label: 'Upper-Outer'},
]
export const TYPES = [
  {value: 'In-Situ', label: 'DCIS'},
  {value: 'IDC', label: 'IDC'},
  {value: 'ILC', label: 'ILC'},
  {value: 'IBC', label: 'IBC'},
  {value: 'Other', label: 'Other'},
]
export const STAGES = [ //I, 'IIA', 'IIB', 'IIIA', 'IIIB', 'IIIC', 'IIINOS', IV, or 0
  {value: '0', label: '0'},
  {value: 'I', label: 'I'},
  {value: 'IIA', label: 'IIA'},
  {value: 'IIB', label: 'IIB'},
  {value: 'IIIA', label: 'IIIA'},
  {value: 'IIIB', label: 'IIIB'},
  {value: 'IIIC', label: 'IIIC'},
  {value: 'IIINOS', label: 'IIINOS'},
  {value: 'IV', label: 'IV'},
]
export const REGIONS = [
  {value: 'Distant', label: 'Distant'},
  {value: 'In-Situ', label: 'In Situ'},
  {value: 'Localized', label: 'Localized'},
  {value: 'Regional', label: 'Regional'},
  {value: 'unk', label: 'Unknown'},
]
export const PREV_TOKEN_COOKIE = '_prev_token_'
export const TOKEN_COOKIE = '_token_'
export const REFRESH_TOKEN_COOKIE = '_refresh_token_'
