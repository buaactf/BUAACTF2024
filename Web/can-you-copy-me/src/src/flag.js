const lhs = [
  'RaTypYkNEouCNNLshAuWuBJytcspElTgWyuVHmCNVVRynJpicklkaUBkrRcxlJBvJFiWYuqvPbdevhBCyIEOxOXaONCzPZzcrRuiIVzVwNRYzhYJCiEkgHMFUWMdVYUY',
  'llNXiHCxxaedKAtsSZcjpGPBfxBxAFVDtqtNupYHFqhWXjmlxcNewZWvjattHSkaxMkDmivjXWYEkYUPpTgsKWHwLhnvzhIwywpOVOjttxPQCEBpfqYLlVHXNJtzFAef',
  'POEehtogwjvvLTkFhRciDHCQjEQyQFRhXDJDcnfWbIjKReoUOzfYHMaFfUHYOomGljaiTcurOEyvqEilcwfkUjIIKVgxxFxAvQgGvYzcMLJytBvOZuvajrEVanuGYUGU',
  'BemSwcRLOKcsPgJqMfoJHifmDOkOlWmyaHZHwpcLdxulGLijabYotNuFsWBobfyoXAeRxugFQbZBEpzAZXbbySTjKiRNnsDsYxIcjbGjPeNqzyCofwBiOPlrNLKxFLAA'
];

const rhs = [
  'yuRTafGYbYKBDRGYHFzANVoXOfowKKPcPaEiYajdCLcJtbdjAwIGMtDvVPWkBDVHbYJRpmyvVfufjgMxTxlRXqCtveAkyalyFznfIPWgZsSuaUgMqHIPXUECwfETKoky',
  'hDrWkqmTOKQSLoxbsGDTQydLYqHJnYIUhjBCczHXtPKkMOtJpeLaaqXzciaAzByLthZIDLbhQETabGEchyeABtfirUoZoOhSWIDhLFSxcQShWuLSuUcqxbKRQjBpawAV',
  'FJvBCaokrJBCdrYNwdSyVjEfGmldNOSTkAOhCUUtwIGvTnBxqxkdDPxKgeSSfQmNLNutcjrfHqYUBeLxnsUNlHDnwXSxkGejbakVcTisiAqnffDhfxzSnFfcPTfKbAmL',
  'msvFTuzLvLkHsHtJsfLzsDFKzKdxhmacDmIWSJDXGhseosCGIhadVFmjxzLutjPdePkvSmeLVaUraELpWkpyeUWNrMLNLFDqgEkqktohSUHwlNHDGgXlgfERqaPMvigZ'
];

export const payload = {
  href: 'https://www.usenix.org/system/files/sec21-musch.pdf',
  part1: lhs, // for method 1
  part2: rhs, // for method 2
  flag: 'BUAACTF{sha256-of-part1-concat-part2}'
};
