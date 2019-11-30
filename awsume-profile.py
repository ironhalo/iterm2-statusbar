#! /usr/bin/env python3

import asyncio
import iterm2
import os


async def main(connection):
    component = iterm2.StatusBarComponent(
        short_description='AWSume Profile',
        detailed_description='The AWS profile as configured by awsume',
        exemplar='AWSume Profile',
        update_cadence=2,
        identifier='com.ironhalo.iterm-statusbar.awsume-profile',
        knobs=[],
    )

    @iterm2.StatusBarRPC
    async def aws_profile(knobs):
        profile = os.getenv('AWSUME_PROFILE',default='')
        return f'aws: {profile}'

    await component.async_register(connection, aws_profile)

iterm2.run_forever(main)
