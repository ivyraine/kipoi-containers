// Copyright (c) Contributors to the Apptainer project, established as
//   Apptainer a Series of LF Projects LLC.
//   For website terms of use, trademark policy, privacy policy and other
//   project policies see https://lfprojects.org/policies
// Copyright (c) 2020, Sylabs Inc. All rights reserved.
// This software is licensed under a 3-clause BSD license. Please consult the
// LICENSE.md file distributed with the sources of this project regarding your
// rights to use or distribute this software.

package apptainer

import (
	"github.com/apptainer/apptainer/internal/pkg/plugin"
	"github.com/apptainer/apptainer/pkg/sylog"
)

// CreatePlugin create the plugin directory skeleton.
func CreatePlugin(dir, name string) error {
	sylog.Debugf("Create %q plugin directory %s", name, dir)
	return plugin.Create(dir, name)
}
