import React from 'react'
import ReactDOM from 'react-dom'
import {
  Divider,
  Image,
  Dimmer,
  Loader,
  Button,
  Select,
} from 'semantic-ui-react'
import useAxios from 'axios-hooks'
import { AxiosError } from 'axios'

const options = [
  {
    key: 'fgsm',
    value: 'fgsm',
    text: 'FGSM',
  },
  {
    key: 'deepfool',
    value: 'deepfool',
    text: 'DeepFool',
  },
]

const useSelect = (): [
  string | null,
  React.Dispatch<React.SetStateAction<string | null>>,
] => {
  const [value, setValue] = React.useState(null as (string | null))

  return [value, setValue]
}

const serverAddress = 'http://localhost:8000/'

const useAttack = (
  attack: string | null,
): [
  { data: any; loading: boolean; error: AxiosError<any> | undefined },
  any,
] => {
  const [{ data, loading, error }, fetch] = useAxios(
    {
      url: attack ? `${serverAddress}${attack}` : serverAddress,
      method: 'GET',
    },
    {
      manual: true,
    },
  )

  return [{ data, loading, error }, fetch]
}

const App = () => {
  const [value, setValue] = useSelect()
  console.log(value)
  const [{ data, loading, error }, fetch] = useAttack(value)

  console.log(data)

  return (
    <>
      {loading ? (
        <Dimmer active>
          <Loader content="Loading" />
        </Dimmer>
      ) : (
        <>
          <Select
            placeholder="Select attack"
            options={options}
            onChange={(e: any, d: any) => setValue(d.value)}
          />
          <Button disabled={value === null} onClick={() => fetch()}>
            Attack!
          </Button>{' '}
          <Divider />
          {data ? (
            <>
              <Image
                src={`data:image/png;base64,${data.original.image}`}
                verticalAlign="middle"
              />{' '}
              <span>{data.original.label}</span>
              <Divider />
              <Image
                src={`data:image/jpeg;base64,${data.adversarial.image}`}
                verticalAlign="middle"
              />{' '}
              <span>{data.adversarial.label}</span>
            </>
          ) : (
            <></>
          )}
        </>
      )}
    </>
  )
}

ReactDOM.render(<App />, document.getElementById('root'))
