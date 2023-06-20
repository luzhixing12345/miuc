'''
*Copyright (c) 2023 All rights reserved
*@description: page processors for specific sites
*@author: Zhixing Lu
*@date: 2023-06-20
*@email: luzhixing12345@163.com
*@Github: luzhixing12345
'''


class Processor:

    def __init__(self) -> None:
        ...

    def __call__(self, url:str):
        return self.parse(url)

    def parse(self, url:str) -> str:
        '''
        override this function for a specific site processor
        '''
        raise NotImplementedError(self.__class__.__name__ + 'should override parse function')



class GithubProcessor(Processor):

    ...



class StackoverflowProcessor(Processor):
    ...