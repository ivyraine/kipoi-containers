// Copyright (c) Contributors to the Apptainer project, established as
//   Apptainer a Series of LF Projects LLC.
//   For website terms of use, trademark policy, privacy policy and other
//   project policies see https://lfprojects.org/policies
// Copyright (c) 2018, Sylabs Inc. All rights reserved.
// This software is licensed under a 3-clause BSD license. Please consult the
// LICENSE.md file distributed with the sources of this project regarding your
// rights to use or distribute this software.

package rlimit

import (
	"testing"

	"github.com/apptainer/apptainer/internal/pkg/test"
)

func TestGetSet(t *testing.T) {
	test.DropPrivilege(t)
	defer test.ResetPrivilege(t)

	cur, max, err := Get("RLIMIT_NOFILE")
	if err != nil {
		t.Error(err)
	}

	if err := Set("RLIMIT_NOFILE", cur, max); err != nil {
		t.Error(err)
	}

	max++

	if err := Set("RLIMIT_NOFILE", cur, max); err == nil {
		t.Errorf("process doesn't have privileges to do that")
	}

	cur, max, err = Get("RLIMIT_FAKE")
	if err == nil {
		t.Errorf("resource limit RLIMIT_FAKE doesn't exist")
	}

	if err := Set("RLIMIT_FAKE", cur, max); err == nil {
		t.Errorf("resource limit RLIMIT_FAKE doesn't exist")
	}
}
